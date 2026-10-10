import argparse
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt

import applicant
import db
from llm_tailor import ensure_pitch


def format_company_panel(company, role_str: str) -> Panel:
    name = company["name"] or ""
    website = company["website"] or ""
    c_type = company["company_type"] or ""
    scope = company["scope"] or ""
    ghana = company["ghana_eligibility"] or ""
    evidence = company["evidence_url"] or ""
    careers = company["careers_url"] or ""
    summary = (company["summary"] or "").strip()
    if len(summary) > 200:
        summary = summary[:197] + "..."
    notes = company["notes"] or ""

    lines = [
        f"[bold]Name:[/bold] {name}    [bold]Type:[/bold] {c_type}",
        f"[bold]Website:[/bold] {website}",
        f"[bold]Role:[/bold] {role_str}",
        f"[bold]Scope/Ghana:[/bold] {scope} | {ghana}",
    ]
    if careers or evidence:
        lines.append(f"[bold]Careers/Evidence:[/bold] {careers or evidence}")
    if summary:
        lines.append(f"[bold]Summary:[/bold] {summary}")
    if notes:
        lines.append(f"[bold yellow]Notes:[/bold yellow] {notes}")

    return Panel("\n".join(lines), title=f"[bold cyan]Company #{company['id']}: {name}[/bold cyan]", expand=False)


def format_contacts_table(contacts: list) -> tuple[Table, bool, bool]:
    """
    Returns (table, has_primary, is_generic_primary)
    """
    table = Table(title="Contacts", expand=False)
    table.add_column("Primary", justify="center")
    table.add_column("Name")
    table.add_column("Title")
    table.add_column("Email")
    table.add_column("Source")
    table.add_column("Kind")
    table.add_column("Verification")
    table.add_column("Confidence")

    has_primary = False
    is_generic_primary = False

    for c in contacts:
        is_prim = bool(c["is_primary"])
        if is_prim:
            has_primary = True
            if c["email_kind"] == "generic":
                is_generic_primary = True
        prim_str = "★" if is_prim else ""
        name = c["full_name"] or ""
        title = c["title"] or ""
        email = c["email"] or ""
        src = c["source"] or ""
        kind = c["email_kind"] or ""
        ver = c["verification_status"] or ""
        conf = str(c["confidence_score"]) if c["confidence_score"] is not None else ""
        table.add_row(prim_str, name, title, email, src, kind, ver, conf)

    return table, has_primary, is_generic_primary


def format_pitch_panel(pitch: dict) -> Panel:
    lead = pitch.get("lead", "")
    bullets = pitch.get("bullets", [])
    provider = pitch.get("provider", "none")
    model = pitch.get("model", "")
    grounded = pitch.get("grounded", False)
    fallback_reason = pitch.get("fallback_reason")

    if grounded:
        badge = "[bold green][GROUNDED][/bold green]"
    else:
        badge = f"[bold red][FALLBACK: {fallback_reason}][/bold red]"

    lines = [
        f"Provider: [bold]{provider}[/bold] ({model}) | Status: {badge}",
        "",
        f"[italic]{lead}[/italic]",
        ""
    ]
    for b in bullets:
        t = b.get("title", "")
        txt = b.get("text", "")
        lines.append(f"• [bold]{t}:[/bold] {txt}")

    return Panel("\n".join(lines), title="[bold magenta]Tailored Pitch[/bold magenta]", expand=False)


def handle_edit_menu(conn, company_id: int, contacts: list, console: Console, ask_fn):
    """
    Sub-menu for editing contact/role:
    Pick an existing contact as primary, add manual contact, or override role title.
    """
    console.print("\n[bold yellow]--- Edit Contact / Role ---[/bold yellow]")
    console.print("1. Set existing contact as primary")
    console.print("2. Add manual contact")
    console.print("3. Override company role title")
    console.print("4. Back")

    choice = ask_fn("Choose an option [1-4]", choices=["1", "2", "3", "4"], default="4")

    if choice == "1":
        if not contacts:
            console.print("[red]No contacts available to set as primary.[/red]")
            return
        contact_ids = [str(c["id"]) for c in contacts]
        console.print("Available contacts:")
        for c in contacts:
            console.print(f"  [{c['id']}] {c['email']} ({c['full_name'] or 'No Name'})")
        cid_str = ask_fn("Enter Contact ID to set as primary", choices=contact_ids)
        db.set_primary_contact(conn, company_id, int(cid_str))
        console.print(f"[green]Set contact {cid_str} as primary.[/green]")

    elif choice == "2":
        email = ask_fn("Enter contact email").strip()
        name = ask_fn("Enter contact name (optional)", default="").strip() or None
        title = ask_fn("Enter contact title (optional)", default="").strip() or None
        kind = ask_fn("Enter email kind [person/departmental]", choices=["person", "departmental"], default="person")
        try:
            cid = db.add_contact(
                conn, company_id, email, full_name=name, title=title,
                source="manual", email_kind=kind, make_primary=True
            )
            console.print(f"[green]Added manual contact {email} (ID {cid}) as primary.[/green]")
        except Exception as e:
            console.print(f"[red]Failed to add contact: {e}[/red]")

    elif choice == "3":
        new_role = ask_fn("Enter new role title").strip()
        if new_role:
            db.update_company(conn, company_id, role_title=new_role)
            console.print(f"[green]Updated role title to: {new_role}[/green]")


def run_review(conn=None, statuses=("Pending",), limit=None, console=None, ask_fn=None):
    """
    Interactive review TUI for company triage.
    """
    close_conn = False
    if conn is None:
        conn = db.connect()
        close_conn = True

    if console is None:
        console = Console()

    if ask_fn is None:
        def ask_fn(prompt, choices=None, default=None):
            return Prompt.ask(prompt, choices=choices, default=default, console=console)

    approved_count = 0
    skipped_count = 0

    try:
        companies = db.list_companies(conn, statuses=statuses, order_by="id")
        if limit:
            companies = companies[:limit]

        for company in companies:
            cid = company["id"]

            while True:
                # Reload fresh company row and contacts each iteration
                comp_row = db.get_company(conn, cid)
                role_str = comp_row["role_title"] or applicant.role_for(comp_row["company_type"])

                # Render Company Panel
                console.print(format_company_panel(comp_row, role_str))

                # Render Contacts Table
                contacts = db.list_contacts(conn, cid)
                ctable, has_primary, is_generic_primary = format_contacts_table(contacts)
                console.print(ctable)

                if not has_primary:
                    console.print("[bold red]WARNING: No primary contact set![/bold red]")
                elif is_generic_primary:
                    console.print("[bold red]WARNING: Primary contact is generic email![/bold red]")

                # Render Pitch Panel
                pitch = ensure_pitch(conn, cid, regenerate=False)
                console.print(format_pitch_panel(pitch))

                # Prompt
                choice = ask_fn(
                    "[A]pprove [S]kip [E]dit contact/role [R]egenerate pitch [N]ext [Q]uit",
                    choices=["a", "s", "e", "r", "n", "q", "A", "S", "E", "R", "N", "Q"],
                    default="n"
                ).upper()

                if choice == "A":
                    # Refuse if no primary contact
                    if not has_primary:
                        console.print("[bold red]Cannot Approve: Company has no primary contact! Please Edit [E] first.[/bold red]")
                        continue
                    db.set_company_status(conn, cid, "Approved")
                    approved_count += 1
                    console.print(f"[green]Company {comp_row['name']} Approved.[/green]")
                    break

                elif choice == "S":
                    db.set_company_status(conn, cid, "Skipped")
                    skipped_count += 1
                    console.print(f"[yellow]Company {comp_row['name']} Skipped.[/yellow]")
                    break

                elif choice == "E":
                    handle_edit_menu(conn, cid, contacts, console, ask_fn)
                    # Loop back to re-render
                    continue

                elif choice == "R":
                    console.print("[cyan]Regenerating pitch...[/cyan]")
                    ensure_pitch(conn, cid, regenerate=True)
                    continue

                elif choice == "N":
                    console.print(f"[dim]Leaving company {comp_row['name']} as is.[/dim]")
                    break

                elif choice == "Q":
                    console.print(f"\n[bold]Triage Summary:[/bold] {approved_count} approved, {skipped_count} skipped.")
                    return {"approved": approved_count, "skipped": skipped_count}

        console.print(f"\n[bold]Triage Summary:[/bold] {approved_count} approved, {skipped_count} skipped.")
        return {"approved": approved_count, "skipped": skipped_count}

    finally:
        if close_conn:
            conn.close()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Interactive review TUI for company triage.")
    parser.add_argument("--status", default="Pending", help="Filter companies by status (default: Pending)")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of companies to review")
    args = parser.parse_args(argv)

    run_review(statuses=(args.status,), limit=args.limit)


if __name__ == "__main__":
    main()
