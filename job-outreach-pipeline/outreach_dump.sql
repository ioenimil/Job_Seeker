BEGIN TRANSACTION;
CREATE TABLE companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE COLLATE NOCASE,
        website TEXT,
        domain TEXT,
        company_type TEXT,
        company_address TEXT,
        scope TEXT,
        ghana_eligibility TEXT,
        evidence_url TEXT,
        careers_url TEXT,
        summary TEXT,
        role_title TEXT,
        pitch TEXT,
        notes TEXT,
        status TEXT NOT NULL DEFAULT 'Pending' CHECK(status IN ('Pending', 'Approved', 'Sent', 'Followup-Sent', 'Replied', 'Bounced', 'Skipped', 'Failed', 'Apply-Online')),
        created_at TEXT,
        updated_at TEXT
    );
INSERT INTO "companies" VALUES(1,'PepaPay','https://pepapay.com','pepapay.com','fintech','Accra, Ghana','local','ghana_based','https://pepapay.com/','',NULL,NULL,NULL,'people_found_no_email','Pending','2026-10-07 00:00:00','2026-10-15 07:44:14');
INSERT INTO "companies" VALUES(2,'Solvane Systems','https://www.solvanesystems.com','solvanesystems.com','fintech','Accra, Ghana','local','ghana_based','https://www.solvanesystems.com/','',NULL,NULL,NULL,'generic_inbox_only','Pending','2026-10-07 00:00:00','2026-10-15 07:44:14');
INSERT INTO "companies" VALUES(3,'DODY Stack','https://dodystack.com','dodystack.com','fintech','Accra, Ghana','local','ghana_based','https://dodystack.com/','',NULL,NULL,NULL,'people_found_no_email','Pending','2026-10-07 00:00:00','2026-10-15 07:44:14');
INSERT INTO "companies" VALUES(4,'SEBBAK Technologies','https://sebbak.com','sebbak.com','fintech','Accra, Ghana','local','ghana_based','https://sebbak.com/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(5,'FinCon Ltd.','https://www.finconghana.com','finconghana.com','fintech','Accra, Ghana','local','ghana_based','https://www.finconghana.com/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(6,'Devarps','https://www.devarps.com','devarps.com','consultancy','Accra, Ghana','local','ghana_based','https://www.devarps.com/','','Devarps is a Ghana-focused software development firm that builds custom software, mobile apps, and SaaS platforms tailored to local realities in Ghana and West Africa. They work with Ghanaian startups, SMEs, and enterprises, handling end-to-end development from architecture to delivery, with an emphasis on offline-first mobile apps, scalable web platforms, and fintech/ERP/CRM-style solutions.

What they do and products/services:
- Custom software development (web and mobile), including ERP/CRM systems and multi-user SaaS platforms
- Mobile apps with offline-first capabilities (Flutter-based)
- Payment gateway and fintech integrations (MTN MoMo, Telecel Cash, Paystack) for web and mobile apps
- Fintech, e-commerce, and enterprise tooling with APIs, data migration, and cloud infrastructure
- Architecture, performance engineering, and reliable, scalable systems
- Transparent project costing with detailed deliverables and milestone-based delivery

Who their customers are:
- Ghanaian startups, SMEs, and enterprises
- Clients needing regionalized solutions built for Ghana/West Africa (payment integration, regulatory considerations, connectivity constraints)
- Teams seeking ownership of code and maintainable, vendor-neutral handovers

Tech stack and capabilities (as highlighted):
- Emphasis on scalable, maintainable architectures designed for Ghanaian realities
- Flutter for offline-first mobile apps; web platforms with aggressive caching and optimized payloads
- Payment integrations with MTN MoMo, Telecel Cash, and Paystack
- Focus on infrastructure-first approach, API design, and robust data compliance
- Transparent, milestone-driven development with ownership of source code, documentation, and assets

Key selling points:
- Built-in understanding of local connectivity, payment systems, and regulatory requirements
- End-to-end ownership: code, docs, and assets transferred to you
- Transparent quotes and timelines; typical MVP in 4–6 weeks, full SaaS/mobile projects in 3–5 months
- Proven ability to deliver investor-ready, scalable MVPs and modern cloud transitions with minimal downtime

If you’re evaluating for a Ghana-focused project, Devarps positions itself as a locally oriented, end-to-end development partner with strong fintech integrations, offline-capable mobile apps, and transparent engagement from discovery to handover.',NULL,'{"lead": "Client work rewards engineers who can drop into an unfamiliar setup and work out what the client actually needs. The harder part is leaving something that still runs after handover. Some of that work:", "bullets": [{"fact_id": "client-facing-delivery", "title": "Client-Facing Delivery", "text": "At Turing I exceeded client KPIs for data accuracy and volume, helping take the team to #1 in dataset quality on client-verified benchmarks; at BoaSoft I shipped a RAG platform built around the client''s own documents."}, {"fact_id": "infrastructure-as-code", "title": "Infrastructure as Code", "text": "I design scalable AWS environments with Terraform and Docker, including a secure multi-tier VPC and modular application layers, so environments are reproducible across clients."}, {"fact_id": "gitops-secrets", "title": "GitOps & Secrets", "text": "I implement GitOps delivery with Argo CD, treating Git as the single source of truth for cluster state, and inject runtime credentials from HashiCorp Vault to keep secrets out of images and repositories."}], "provider": "none", "model": "deterministic", "grounded": true, "fallback_reason": null, "generated_at": "2026-10-11 06:02:10"}','restarted: first email only reached hr@devarps.com','Sent','2026-10-07 00:00:00','2026-10-11 06:34:01');
INSERT INTO "companies" VALUES(7,'Exquode','https://www.exquode.com','exquode.com','consultancy','Accra, Ghana','local','ghana_based','https://www.exquode.com/','',NULL,NULL,NULL,'generic_inbox_only','Pending','2026-10-07 00:00:00','2026-10-15 07:44:14');
INSERT INTO "companies" VALUES(8,'Gamma Technologies','https://gammatechgh.com','gammatechgh.com','consultancy','Accra, Ghana','local','ghana_based','https://gammatechgh.com/','',NULL,NULL,NULL,'people_found_no_email','Pending','2026-10-07 00:00:00','2026-10-15 07:44:14');
INSERT INTO "companies" VALUES(9,'TriAxis Technologies','https://triaxistechnologies.com','triaxistechnologies.com','consultancy','Accra, Ghana','local','ghana_based','https://triaxistechnologies.com/','',NULL,NULL,NULL,'people_found_no_email','Pending','2026-10-07 00:00:00','2026-10-15 07:44:14');
INSERT INTO "companies" VALUES(10,'Apex-Meta','https://apex-meta.com','apex-meta.com','consultancy','Accra, Ghana','local','ghana_based','https://apex-meta.com/','',NULL,NULL,NULL,'generic_inbox_only','Pending','2026-10-07 00:00:00','2026-10-15 07:44:14');
INSERT INTO "companies" VALUES(11,'Infotype Ghana','https://infotypeghana.com','infotypeghana.com','consultancy','Accra, Ghana','local','ghana_based','https://infotypeghana.com/','',NULL,NULL,NULL,'generic_inbox_only','Pending','2026-10-07 00:00:00','2026-10-11 05:39:28');
INSERT INTO "companies" VALUES(12,'Zilo','https://zilotechnologies.com','zilotechnologies.com','consultancy','Accra, Ghana','local','ghana_based','https://zilotechnologies.com/','',NULL,NULL,NULL,'people_found_no_email','Pending','2026-10-07 00:00:00','2026-10-11 05:39:28');
INSERT INTO "companies" VALUES(13,'ThinkingTec','https://thinkingtec.com','thinkingtec.com','consultancy','Accra, Ghana','local','ghana_based','https://thinkingtec.com/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(14,'Wan Tech Solutions','https://wantechsolutions.com','wantechsolutions.com','consultancy','Accra, Ghana','local','ghana_based','https://wantechsolutions.com/','',NULL,NULL,NULL,'people_found_no_email','Pending','2026-10-07 00:00:00','2026-10-11 05:39:28');
INSERT INTO "companies" VALUES(15,'eSolutions Consulting','https://esolutionsghana.com','esolutionsghana.com','consultancy','Accra, Ghana','local','ghana_based','https://esolutionsghana.com/','','Summary:
- What they do: eSolutions Consulting helps organizations assess, migrate, secure, and operate Microsoft environments (Azure, Microsoft 365) and provides AI readiness and managed IT services. They position themselves as a cloud and AI transformation partner focused on secure, scalable Microsoft cloud solutions to drive agility and intelligent growth.
- Products/services they build or offer:
  - Cloud Transformation: design, migration, and optimization on Microsoft Azure
  - Cybersecurity & Compliance: end-to-end security (identity, endpoint protection, regulatory compliance)
  - AI & Intelligent Solutions: automation, insights, and AI-enabled business applications
  - Modern Workplace: Microsoft 365, Teams, and collaboration tooling
  - Business Applications: digitization and automation with tailored apps, workflows, data insights
  - IT Consulting & Enterprise Architecture: strategic advisory, architecture design, digital transformation planning
  - Managed Services & Support: proactive monitoring, optimization, 24/7 support
  - Industry-focused cloud/security/digital transformation solutions
  - Specific offerings/initiatives: SmartWorkplace v5.0, Nuvola9, Enterprise Architecture, Business Re-engineering, IT Transformation
- Who their customers are: Organizations seeking Microsoft cloud adoption and AI enablement across industries; they tailor solutions to industry-specific regulatory and operational needs.
- Tech stack (inferred from positioning): Microsoft-centric stack including Azure cloud, Microsoft 365, Teams; security tooling for identity and endpoints; data/AI capabilities integrated into Microsoft ecosystem; enterprise architecture and IT transformation practices around Microsoft cloud solutions. They emphasize cloud, AI readiness, security, and managed services within the Microsoft environment.',NULL,'{"lead": "Client work rewards engineers who can drop into an unfamiliar setup and work out what the client actually needs. The harder part is leaving something that still runs after handover. Some of that work:", "bullets": [{"fact_id": "client-facing-delivery", "title": "Client-Facing Delivery", "text": "At Turing I exceeded client KPIs for data accuracy and volume, helping take the team to #1 in dataset quality on client-verified benchmarks; at BoaSoft I shipped a RAG platform built around the client''s own documents."}, {"fact_id": "infrastructure-as-code", "title": "Infrastructure as Code", "text": "I design scalable AWS environments with Terraform and Docker, including a secure multi-tier VPC and modular application layers, so environments are reproducible across clients."}, {"fact_id": "gitops-secrets", "title": "GitOps & Secrets", "text": "I implement GitOps delivery with Argo CD, treating Git as the single source of truth for cluster state, and inject runtime credentials from HashiCorp Vault to keep secrets out of images and repositories."}], "provider": "none", "model": "deterministic", "grounded": true, "fallback_reason": null, "generated_at": "2026-10-11 06:02:22"}','restarted: first email only reached careers@esolutionsghana.com','Sent','2026-10-07 00:00:00','2026-10-11 06:34:52');
INSERT INTO "companies" VALUES(16,'Digits & Data Limited','https://digitsndata.com','digitsndata.com','consultancy','Accra, Ghana','local','ghana_based','https://digitsndata.com/','','Digits & Data Limited (DnD) is a leading ICT consulting firm headquartered in Accra, Ghana, focused on empowering Africa through technology-driven transformation.

What they do
- Provide comprehensive ICT consulting and technology solutions to businesses, governments, and organizations across Africa.
- Help clients achieve digital transformation and future-proof operations through innovative, scalable solutions.

Products and services (core offerings)
- Digital Financial Services (DFS): omnichannel banking and payments platform with secure, scalable financial services for retail and corporate clients.
- Cybersecurity & IT Risk: end-to-end security solutions to protect against cyber threats.
- Enterprise Resource Planning (ERP): cloud-based ERP unifying finance, procurement, inventory, CRM, supply chain, and sales.
- Cloud & Datacenter: modern cloud infrastructure and datacenter services.
- Data & AI: data analytics, AI-driven automation, and insights generation.
- Blockchain & Edge: blockchain and edge computing for decentralized apps.
- Oracle NetSuite: Premier Oracle NetSuite partner delivering unified cloud ERP for finance, CRM, supply chain, and more in West Africa.
- Advansio Solutions (productized platforms via R&D arm):
  - AdvansPay: corporate payment app with invoicing, multi-wallets, QR/Paylink, reconciliation.
  - AdvansCollect: bank-hosted platform for invoicing, bulk payments, collections with controls and reporting.
  - Digital Financial Services (DFS): omnichannel banking (retail and corporate) with internet banking, mobile apps, USSD, cards, wallets, loans, alerts.
  - AdvansIntegration: cross-border, continent-wide bank connectivity for payments.
- AI-powered solutions across industries: practical AI applications in financial services (fraud detection, credit scoring, risk modeling, personalized digital banking), healthcare analytics, mining/industrial analytics, and enterprise automation (vision, predictive maintenance, etc.).

Who their customers are
- Businesses, governments, and organizations across Africa seeking ICT modernization, digital financial services, ERP, cybersecurity, and data/AI capabilities.
- Notably active in West Africa with NetSuite/Oracle deployments and cross-border financial connectivity.

Tech stack and capabilities (highlights)
- ERP/Cloud: Oracle NetSuite, cloud ERP, broader cloud and data center services.
- Financial tech: DFS platforms, AdvansPay, AdvansCollect, bank connectivity via AdvansIntegration.
- Security: comprehensive IT risk and cybersecurity offerings.
- Data & AI: analytics, AI solutions, industry-specific AI use cases.
- Blockchain & Edge: blockchain and edge computing for decentralized apps.
- Industry-specific software: fintech, payments, collections, banking platforms, and regulatory/enterprise software needs.

Bottom line
DnD is a Pan-African ICT consulting firm delivering end-to-end technology solutions—from ERP and cloud to cybersecurity, data/AI, and specialized fintech platforms (Advansio) and Oracle NetSuite implementations—serving private sector companies, government bodies, and organizations across Africa.',NULL,'{"lead": "Client work rewards engineers who can drop into an unfamiliar setup and work out what the client actually needs. The harder part is leaving something that still runs after handover. Some of that work:", "bullets": [{"fact_id": "client-facing-delivery", "title": "Client-Facing Delivery", "text": "At Turing I exceeded client KPIs for data accuracy and volume, helping take the team to #1 in dataset quality on client-verified benchmarks; at BoaSoft I shipped a RAG platform built around the client''s own documents."}, {"fact_id": "infrastructure-as-code", "title": "Infrastructure as Code", "text": "I design scalable AWS environments with Terraform and Docker, including a secure multi-tier VPC and modular application layers, so environments are reproducible across clients."}, {"fact_id": "gitops-secrets", "title": "GitOps & Secrets", "text": "I implement GitOps delivery with Argo CD, treating Git as the single source of truth for cluster state, and inject runtime credentials from HashiCorp Vault to keep secrets out of images and repositories."}], "provider": "none", "model": "deterministic", "grounded": true, "fallback_reason": null, "generated_at": "2026-10-11 06:02:46"}','restarted: first email only reached info@digitsndata.com','Sent','2026-10-07 00:00:00','2026-10-11 06:35:31');
INSERT INTO "companies" VALUES(17,'Phyled Solutions','https://phyledsolutions.com','phyledsolutions.com','consultancy','Accra, Ghana','local','ghana_based','https://phyledsolutions.com/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(18,'De-MannyTech Consult','https://www.demannytechconsult.com','demannytechconsult.com','consultancy','Accra, Ghana','local','ghana_based','https://www.demannytechconsult.com/','',NULL,NULL,NULL,'generic_inbox_only','Pending','2026-10-07 00:00:00','2026-10-11 05:39:28');
INSERT INTO "companies" VALUES(19,'Mawulikode Consulting','https://mawulikode.com','mawulikode.com','consultancy','Accra, Ghana','local','ghana_based','https://mawulikode.com/','','Summary:
- What they do: Mawulikode positions itself as an AWS Solutions partner in Ghana, guiding cloud adoption, migration, application development, and ongoing AWS account and IT management.
- Products/Services they build or offer:
  - Cloud Adoption: strategic planning and implementation for digital transformation.
  - Cloud Migration: migrate infrastructure to AWS with minimal downtime and optimized performance.
  - Application Development: building scalable, cloud-native applications on AWS.
  - AWS Account Management: setup, security configuration, and ongoing AWS management.
  - General IT Consulting: IT strategy aligned with business goals.
- Who their customers are: While not explicitly named in the provided content, the emphasis on cloud migration, application development, and IT consulting suggests they target businesses seeking AWS-based cloud transformation and scalable application solutions, likely in Ghana.
- Tech stack: The content references AWS-focused services and cloud-native development, but does not list specific technologies or tools. The inferred stack centers on AWS services (e.g., cloud infrastructure, security, application hosting) and modern cloud-native development practices.

If you need, I can tailor this to emphasize any particular service or provide a client-focused profile once you have examples of their customers or projects.',NULL,'{"lead": "Client work rewards engineers who can drop into an unfamiliar setup and work out what the client actually needs. The harder part is leaving something that still runs after handover. Some of that work:", "bullets": [{"fact_id": "client-facing-delivery", "title": "Client-Facing Delivery", "text": "At Turing I exceeded client KPIs for data accuracy and volume, helping take the team to #1 in dataset quality on client-verified benchmarks; at BoaSoft I shipped a RAG platform built around the client''s own documents."}, {"fact_id": "infrastructure-as-code", "title": "Infrastructure as Code", "text": "I design scalable AWS environments with Terraform and Docker, including a secure multi-tier VPC and modular application layers, so environments are reproducible across clients."}, {"fact_id": "gitops-secrets", "title": "GitOps & Secrets", "text": "I implement GitOps delivery with Argo CD, treating Git as the single source of truth for cluster state, and inject runtime credentials from HashiCorp Vault to keep secrets out of images and repositories."}], "provider": "none", "model": "deterministic", "grounded": true, "fallback_reason": null, "generated_at": "2026-10-11 06:03:03"}','restarted: first email only reached info@mawulikode.com','Sent','2026-10-07 00:00:00','2026-10-11 06:36:31');
INSERT INTO "companies" VALUES(20,'YaakaCorp Ent.','https://yaakacorp.com','yaakacorp.com','consultancy','Accra, Ghana','local','ghana_based','https://yaakacorp.com/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(21,'AITS','https://aitsapp.com','aitsapp.com','consultancy','Accra, Ghana','local','ghana_based','https://aitsapp.com/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(22,'IPMC','https://ipmcghana.com','ipmcghana.com','consultancy','Accra, Ghana','local','ghana_based','https://ipmcghana.com/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(23,'Jesi AI','https://www.jesiai.com','jesiai.com','ai','Ghana','local','ghana_based','https://www.jesiai.com/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(24,'Ciphonyx Solutions Ltd','https://ciphonyx.com','ciphonyx.com','consultancy','Kumasi, Ghana','local','ghana_based','https://ciphonyx.com/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(25,'Acloe Technologies','https://acloe.com','acloe.com','general_startup','Kumasi, Ghana','local','ghana_based','https://acloe.com/','',NULL,NULL,NULL,'restarted: first email only reached hello@acloe.com','Pending','2026-10-07 00:00:00','2026-10-11 05:22:40');
INSERT INTO "companies" VALUES(26,'Team Programmers','https://teamprogrammers.com','teamprogrammers.com','general_startup','Kumasi, Ghana','local','ghana_based','https://teamprogrammers.com/','',NULL,NULL,NULL,'generic_inbox_only','Pending','2026-10-07 00:00:00','2026-10-11 05:39:28');
INSERT INTO "companies" VALUES(27,'Samasoft Technologies','https://samasoftech.net','samasoftech.net','general_startup','Kumasi, Ghana','local','ghana_based','https://samasoftech.net/','',NULL,NULL,NULL,'generic_inbox_only','Pending','2026-10-07 00:00:00','2026-10-11 05:39:28');
INSERT INTO "companies" VALUES(28,'Emmaktech Networks','https://emmaktech.com','emmaktech.com','general_startup','Kumasi, Ghana','local','ghana_based','https://emmaktech.com/','',NULL,NULL,NULL,'people_found_no_email','Pending','2026-10-07 00:00:00','2026-10-11 05:39:28');
INSERT INTO "companies" VALUES(29,'Trinity Software Center','https://web.trinitysoftwarecenter.com','web.trinitysoftwarecenter.com','ai','Kumasi, Ghana','local','ghana_based','https://web.trinitysoftwarecenter.com/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(30,'Prime Info Tech Solutions','https://www.primeinfo.tech','primeinfo.tech','consultancy','Kumasi, Ghana','local','ghana_based','https://www.primeinfo.tech/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(31,'Telecel Ghana','https://telecel.com.gh','telecel.com.gh','isp','Ghana','local','ghana_based','https://telecel.com.gh/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(32,'AT Ghana','https://www.at.com.gh','at.com.gh','isp','Ghana','local','ghana_based','https://www.at.com.gh/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(33,'Celltel Networks Limited','https://celltel.com.gh','celltel.com.gh','isp','Dzorwulu, Accra, Ghana','local','ghana_based','https://celltel.com.gh/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(34,'Telenet Ghana','https://telenet.com.gh','telenet.com.gh','isp','Legon, Accra, Ghana','local','ghana_based','https://telenet.com.gh/','',NULL,NULL,NULL,'people_found_no_email','Pending','2026-10-07 00:00:00','2026-10-11 05:39:28');
INSERT INTO "companies" VALUES(35,'Telesol','https://telesol.com.gh','telesol.com.gh','isp','Adabraka, Accra, Ghana','local','ghana_based','https://telesol.com.gh/','',NULL,NULL,NULL,'people_found_no_email','Pending','2026-10-07 00:00:00','2026-10-11 05:39:28');
INSERT INTO "companies" VALUES(36,'Boldnet Internet Solutions','https://boldnetgh.com','boldnetgh.com','isp','Adenta, Accra, Ghana','local','ghana_based','https://boldnetgh.com/','',NULL,NULL,NULL,'generic_inbox_only','Pending','2026-10-07 00:00:00','2026-10-11 05:39:28');
INSERT INTO "companies" VALUES(37,'Mobobi','https://www.mobobi.com','mobobi.com','ai','Accra, Ghana','local','ghana_based','https://www.mobobi.com/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(38,'Coratech AI','https://coratechai.com','coratechai.com','ai','Accra, Ghana','local','ghana_based','https://coratechai.com/','',NULL,NULL,NULL,'generic_inbox_only','Pending','2026-10-07 00:00:00','2026-10-11 05:39:28');
INSERT INTO "companies" VALUES(39,'Candoship Ltd','https://candoship.com','candoship.com','ai','Ghana','local','ghana_based','https://candoship.com/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(40,'Mewokrom','https://mewokrom.com','mewokrom.com','ai','Accra, Ghana','local','ghana_based','https://mewokrom.com/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(41,'Kaizen Technologies','https://kaizentech.tech','kaizentech.tech','ai','Accra, Ghana','local','ghana_based','https://kaizentech.tech/','',NULL,NULL,NULL,'generic_inbox_only','Replied','2026-10-07 00:00:00','2026-10-15 06:58:50');
INSERT INTO "companies" VALUES(42,'Jasma Technologies','https://jasmaai.com','jasmaai.com','ai','Accra, Ghana','local','ghana_based','https://jasmaai.com/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(43,'NiiOsa Labs','https://www.niiosalabs.com','niiosalabs.com','ai','Accra, Ghana','local','ghana_based','https://www.niiosalabs.com/','',NULL,NULL,NULL,NULL,'Followup-Sent','2026-10-07 00:00:00','2026-10-15 07:14:40');
INSERT INTO "companies" VALUES(44,'Boldstep Hiven','https://boldstephiven.com','boldstephiven.com','ai','Accra, Ghana','local','ghana_based','https://boldstephiven.com/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(45,'SeleScribe','https://selescribe.com','selescribe.com','general_startup','','remote','africa_region','https://selescribe.com/careers','https://selescribe.com/careers',NULL,NULL,NULL,'restarted: first email only reached careers@selescribe.com','Pending','2026-10-07 00:00:00','2026-10-11 05:22:40');
INSERT INTO "companies" VALUES(46,'PhotonAI','https://photonai.ai','photonai.ai','ai','','remote','africa_region','https://photonai.ai/careers.html','https://photonai.ai/careers.html',NULL,NULL,NULL,'restarted: first email only reached engineering@photonai.ai','Pending','2026-10-07 00:00:00','2026-10-11 05:22:40');
INSERT INTO "companies" VALUES(47,'Deimos','https://www.deimos.io','deimos.io','general_startup','','remote','explicit_ghana','https://www.deimos.io/about/careers','https://www.deimos.io/about/careers',NULL,NULL,NULL,NULL,'Apply-Online','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(48,'M-KOPA','https://www.m-kopa.com','m-kopa.com','fintech','','remote','explicit_ghana','https://jobs.ashbyhq.com/M-KOPA/0c0fdef0-61b7-4f7d-bd56-c09d66471396/application','https://www.m-kopa.com/careers',NULL,NULL,NULL,NULL,'Apply-Online','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(49,'Risk Labs','https://risklabs.foundation','risklabs.foundation','fintech','','remote','worldwide','https://jobs.ashbyhq.com/risklabs','https://jobs.ashbyhq.com/risklabs',NULL,NULL,NULL,NULL,'Apply-Online','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(50,'Celsus','https://www.celsusos.com','celsusos.com','general_startup','Accra, Ghana','local','ghana_based','https://www.celsusos.com/careers/backend-engineer','https://www.celsusos.com/careers',NULL,NULL,NULL,'generic_inbox_only','Pending','2026-10-07 00:00:00','2026-10-11 05:39:28');
INSERT INTO "companies" VALUES(51,'Railway','https://railway.com','railway.com','general_startup','','remote','worldwide','https://jobs.ashbyhq.com/railway/b8072f95-043f-404d-a313-f0bdf8dd3c81','https://railway.com/careers',NULL,NULL,NULL,NULL,'Apply-Online','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(52,'Georion','https://georion.app','georion.app','ai','','remote','worldwide','https://georion.app/careers','https://georion.app/careers',NULL,NULL,NULL,NULL,'Apply-Online','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(53,'NYAMAI NEXUS GROUP','https://www.nyamainexus.com','nyamainexus.com','ai','','remote','africa_region','https://www.nyamainexus.com/careers','https://www.nyamainexus.com/careers',NULL,NULL,NULL,NULL,'Apply-Online','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(54,'AI Labs Africa','https://ailabsafrica.com','ailabsafrica.com','ai','','remote','explicit_ghana','https://ailabsafrica.com/careers','https://ailabsafrica.com/careers',NULL,NULL,NULL,NULL,'Apply-Online','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(55,'HostNowNow','https://hostnownow.com','hostnownow.com','general_startup','','remote','africa_region','https://hostnownow.com/company/careers','https://hostnownow.com/company/careers','HostNowNow positions itself as “The African AI Cloud” aimed at African developers and teams. It offers an all-in-one platform to build, deploy, and manage web apps and AI-enabled services with a focus on speed and ease of use. Key offerings and capabilities:

What they do
- Provide cloud hosting and website/infrastructure services tailored for Africa.
- Combine domains, hosting, managed WordPress, and AI-enabled deployment tools under one account.
- Emphasize rapid deployment of apps and automated workflows with AI integration.

Products and services
- HNN Flux: Git-driven deployment with automatic builds, no traditional pipelines. Includes managed databases and an OpenAI-compatible AI gateway. GitHub integration for branch-based deployments.
- Managed WordPress: Fully managed, scalable WordPress hosting.
- Azure Web Hosting: Upgrades from traditional hosting, offering hPanel simplicity with Azure reliability and security.
- Business Email: Domain-based professional mailboxes with spam filtering and ample storage.
- All-in-one bundles: Domains, deployments, AI credits, SSL, email, and WordPress site included at no extra cost. Flux deployments include monthly AI gateway credits.
- Deployment support for multiple stacks: Next.js, Node.js, Python, Laravel, WordPress, etc., with automatic provisioning of databases and AI gateway.

What they build for customers
- Websites and web apps with built-in AI gateways and managed infrastructure.
- Automated deployment workflows from code repositories.
- Managed hosting for WordPress sites and Azure-backed hosting for higher reliability.
- Email and SSL/security, plus scalable hosting with automatic backups and scaling.

Who their customers are
- Teams and developers in Africa seeking a fast, integrated cloud for building and shipping websites, backends, and AI-powered flows.
- Businesses needing a one-stop platform for domains, hosting, AI credits, and WordPress sites.

Tech stack (implied)
- Git-based deployment pipelines (Flux) with automatic builds upon pushes.
- AI gateway compatible with OpenAI-like APIs for AI workloads.
- Managed databases integrated with deployed apps.
- Web hosting stacks including Next.js, Node.js, Python, Laravel, WordPress.
- SSL/HTTPS, domain management, and cloud hosting infrastructure (Azure-backed hosting option).

If you want, I can tailor this to answer a specific angle (e.g., focus on developers, enterprise, or Africa-focused benefits) or compare to typical alternatives.',NULL,'{"lead": "Startups need to ship fast without the platform falling over. Automating the slow, error-prone parts is how I make both possible:", "bullets": [{"fact_id": "infrastructure-velocity", "title": "Infrastructure Velocity", "text": "I provision production-ready AWS infrastructure with Terraform and Docker, including a secure multi-tier VPC and modular application layers."}, {"fact_id": "fast-feedback-loops", "title": "Fast Feedback Loops", "text": "I built a cost-optimized Jenkins CI/CD engine with EC2 Spot agents that auto-scale with build queue depth, speeding up developer feedback while cutting compute cost."}, {"fact_id": "developer-self-service", "title": "Developer Self-Service", "text": "I deployed Prometheus, Loki, Grafana, and Jaeger with self-service dashboards that give developers on-demand insight into their environments and error logs."}], "provider": "none", "model": "deterministic", "grounded": true, "fallback_reason": null, "generated_at": "2026-10-11 06:03:12"}','restarted: first email only reached careers@hostnownow.com','Sent','2026-10-07 00:00:00','2026-10-11 06:37:24');
INSERT INTO "companies" VALUES(56,'OSOMEC Global Tech','https://osomecglobaltech.com','osomecglobaltech.com','general_startup','','remote','africa_region','https://osomecglobaltech.com/careers','https://osomecglobaltech.com/careers',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(57,'Arfa Technology','https://arfatechnology.com','arfatechnology.com','general_startup','','remote','africa_region','https://arfatechnology.com/careers/','https://arfatechnology.com/careers/',NULL,NULL,NULL,NULL,'Apply-Online','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(58,'Branch International','https://branch.co','branch.co','fintech','','remote','africa_region','https://builtin.com/job/backend-software-engineer-remote-nigeria/4562188','https://branch.co/careers',NULL,NULL,NULL,NULL,'Apply-Online','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(59,'Mazzuma','https://mazzuma.com','mazzuma.com','fintech','Accra, Ghana','local','ghana_based','https://www.startuplist.africa/startups/mazzuma','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(60,'Nvoicia','https://nvoicia.com','nvoicia.com','fintech','Accra, Ghana','local','ghana_based','https://www.startuplist.africa/startups/nvoicia','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(61,'Wayve Mobility','https://wayve.africa','wayve.africa','fintech','Accra, Ghana','local','ghana_based','https://wayve.africa/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(62,'GIT Plus','https://gitplus.app','gitplus.app','consultancy','Accra, Ghana','local','ghana_based','https://gitplus.app/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(63,'Orgmento','https://orgmento.com','orgmento.com','consultancy','Accra, Ghana','local','ghana_based','https://orgmento.com/','','Orgmento is a software engineering and data sciences company based in Accra, Ghana. They augment partner organizations’ software and data teams by supplying individual engineers, data scientists, or dedicated multi-functional teams for long- or short-term projects. They design, build, and optimize scalable enterprise, financial, governmental, and science-based systems, with a strong emphasis on social impact in Africa and local talent development.

Products/Services they build:
- Custom software and data platforms
- Software architecture reviews and holistic architecture recommendations
- Data management, data engineering, and data science services (data gathering, organizing, securing, analyzing, and making data FAIR)
- Quality assurance and testing
- Software product development, internal optimization, and process automation
- System audits and performance/scalability improvements

Who their customers are:
- Partner organizations across international and local ecosystems
- Enterprises needing software and data capabilities
- Governmental, financial, scientific, and other organizations requiring scalable, reliable systems
- Clients seeking dedicated, long-term software/data teams or extended augmentation

Tech stack (inferred from services offered):
- Software engineering and architecture for scalable systems (likely standard enterprise stacks)
- Data science and data engineering, with emphasis on data management and making data FAIR (implies use of data warehousing, ETL, analytics, ML/AI workflows)
- Quality assurance practices
Note: The site does not specify exact technologies (programming languages, frameworks, cloud providers), so exact tech stack details aren’t listed.

Top value proposition:
- Local talent augmentation from top universities
- Long-term, sustainable partnerships
- Alignment with partners’ strategic goals and social impact in Africa
- Focus on clarity, collaboration, and measurable outcomes

If you want, I can tailor this to a specific audience (e.g., potential clients in finance vs. government) or search for more concrete tech-stack details if available.',NULL,'{"lead": "Client work rewards engineers who can drop into an unfamiliar setup and work out what the client actually needs. The harder part is leaving something that still runs after handover. Some of that work:", "bullets": [{"fact_id": "client-facing-delivery", "title": "Client-Facing Delivery", "text": "At Turing I exceeded client KPIs for data accuracy and volume, helping take the team to #1 in dataset quality on client-verified benchmarks; at BoaSoft I shipped a RAG platform built around the client''s own documents."}, {"fact_id": "infrastructure-as-code", "title": "Infrastructure as Code", "text": "I design scalable AWS environments with Terraform and Docker, including a secure multi-tier VPC and modular application layers, so environments are reproducible across clients."}, {"fact_id": "gitops-secrets", "title": "GitOps & Secrets", "text": "I implement GitOps delivery with Argo CD, treating Git as the single source of truth for cluster state, and inject runtime credentials from HashiCorp Vault to keep secrets out of images and repositories."}], "provider": "none", "model": "deterministic", "grounded": true, "fallback_reason": null, "generated_at": "2026-10-11 06:03:24"}','restarted: first email only reached hello@orgmento.com','Sent','2026-10-07 00:00:00','2026-10-11 06:38:15');
INSERT INTO "companies" VALUES(64,'TekSol Limited','https://www.teksol.com.gh','teksol.com.gh','general_startup','Accra, Ghana','local','ghana_based','https://www.teksol.com.gh/','',NULL,NULL,NULL,'people_found_no_email','Bounced','2026-10-07 00:00:00','2026-10-15 06:57:50');
INSERT INTO "companies" VALUES(65,'Ammeter Labs','https://ammeterlabs.com','ammeterlabs.com','general_startup','Accra, Ghana','local','ghana_based','https://ammeterlabs.com/','',NULL,NULL,NULL,'generic_inbox_only','Pending','2026-10-07 00:00:00','2026-10-11 05:39:28');
INSERT INTO "companies" VALUES(66,'Excedi Limited','https://excedi.com','excedi.com','general_startup','Accra, Ghana','local','ghana_based','https://excedi.com/','',NULL,NULL,NULL,'people_found_no_email','Pending','2026-10-07 00:00:00','2026-10-11 05:39:28');
INSERT INTO "companies" VALUES(67,'Aetheris Core','https://aetheriscore.com','aetheriscore.com','general_startup','Accra, Ghana','local','ghana_based','https://aetheriscore.com/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(68,'Medirevs','https://www.medirevs.com','medirevs.com','general_startup','Accra, Ghana','local','ghana_based','https://www.medirevs.com/','',NULL,NULL,NULL,'people_found_no_email','Pending','2026-10-07 00:00:00','2026-10-11 05:39:28');
INSERT INTO "companies" VALUES(69,'Voima','https://voimainitiative.com','voimainitiative.com','ai','Accra, Ghana','local','ghana_based','https://voimainitiative.com/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(70,'iKolilu','https://ikolilu.com','ikolilu.com','general_startup','Accra, Ghana','local','ghana_based','https://ikolilu.com/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(71,'NanorLearn','https://nanorlearn.com','nanorlearn.com','general_startup','Accra, Ghana','local','ghana_based','https://nanorlearn.com/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(72,'QKnow EdTech','https://qknowedtech.com','qknowedtech.com','general_startup','Accra, Ghana','local','ghana_based','https://linkedin.com/company/qknow-edtech','',NULL,NULL,NULL,'people_found_no_email','Pending','2026-10-07 00:00:00','2026-10-11 05:39:28');
INSERT INTO "companies" VALUES(73,'ADDNET','https://addnett.com','addnett.com','consultancy','Accra, Ghana','local','ghana_based','https://addnett.com/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(74,'Edfrica','https://www.edfrica.com','edfrica.com','general_startup','Accra, Ghana','local','ghana_based','https://www.edfrica.com/','',NULL,NULL,NULL,'people_found_no_email','Pending','2026-10-07 00:00:00','2026-10-11 05:39:28');
INSERT INTO "companies" VALUES(75,'WeMo Technologies Ghana','https://www.wemotechnologies.com','wemotechnologies.com','general_startup','Accra, Ghana','local','ghana_based','https://www.wemotechnologies.com/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(76,'EDVES Ghana','https://gh.edves.net','gh.edves.net','general_startup','Accra, Ghana','local','ghana_based','https://gh.edves.net/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(77,'SyllabusGH','https://syllabusgh.com','syllabusgh.com','general_startup','Accra, Ghana','local','ghana_based','https://linkedin.com/company/syllabusgh','',NULL,NULL,NULL,'people_found_no_email','Pending','2026-10-07 00:00:00','2026-10-11 05:39:28');
INSERT INTO "companies" VALUES(78,'eCampus','https://ecampus.camp','ecampus.camp','general_startup','Accra, Ghana','local','ghana_based','https://vc4a.com/ventures/myecampus-net/?lang=en','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(79,'Tudu Africa','https://tudu.africa','tudu.africa','general_startup','Accra, Ghana','local','ghana_based','https://tudu.africa/about','',NULL,NULL,NULL,'people_found_no_email','Pending','2026-10-07 00:00:00','2026-10-11 05:39:28');
INSERT INTO "companies" VALUES(80,'Proxymove','https://proxymove.com','proxymove.com','general_startup','Accra, Ghana','local','ghana_based','https://proxymove.com/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(81,'Shopbeta','https://shopbeta.com.gh','shopbeta.com.gh','general_startup','Accra, Ghana','local','ghana_based','https://shopbeta.com.gh/','',NULL,NULL,NULL,'people_found_no_email','Pending','2026-10-07 00:00:00','2026-10-11 05:39:28');
INSERT INTO "companies" VALUES(82,'Tezeon Ghana','https://tezeon.com','tezeon.com','general_startup','Accra, Ghana','local','ghana_based','https://tezeon.com/','',NULL,NULL,NULL,'people_found_no_email','Pending','2026-10-07 00:00:00','2026-10-11 05:39:28');
INSERT INTO "companies" VALUES(83,'Salliba','https://salliba.com','salliba.com','general_startup','Accra, Ghana','local','ghana_based','https://salliba.com/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(84,'GHVENDORS','https://ghvendors.com','ghvendors.com','general_startup','Accra, Ghana','local','ghana_based','https://ghvendors.com/','',NULL,NULL,NULL,'generic_inbox_only','Pending','2026-10-07 00:00:00','2026-10-11 05:39:28');
INSERT INTO "companies" VALUES(85,'CITSYS','https://citsys.com','citsys.com','consultancy','Accra, Ghana','local','ghana_based','https://citsys.com/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(86,'Virtual Infosec Africa','https://www.virtualinfosecafrica.com','virtualinfosecafrica.com','consultancy','Accra, Ghana','local','ghana_based','https://www.virtualinfosecafrica.com/','','Summary:
Virtual Infosec Africa (VIA) is a wholly Ghanaian cybersecurity company (established 2008) specializing in tailored information security solutions and services across Africa. They offer 24/7, ISO/IEC 27001-certified Security Operations Center (SOC) and managed security services, acting as an extension of clients’ teams. Core offerings include information security risk assessments, vulnerability assessment and penetration testing, social engineering, digital forensics, security training and awareness, and continuous SOC monitoring. They partner with top global OEMs to deliver world-class security solutions and claim 200+ clients.

What they build/offer:
- Managed information and cybersecurity services
- 24/7 intelligent SOC operations (ISO/IEC 27001 certified)
- Information security risk assessments
- Vulnerability assessment and penetration testing
- Social engineering testing
- Digital forensics
- Security training and awareness programs

Customers:
- More than 200 clients across Africa (specific industries not listed on the page)

Tech stack:
- The site does not specify exact technologies or tools; they emphasize ISO/IEC 27001 certified SOC, partnerships with top OEMs, and a team of certified security experts. No explicit software, platforms, or hardware brands are named.',NULL,'{"lead": "Client work rewards engineers who can drop into an unfamiliar setup and work out what the client actually needs. The harder part is leaving something that still runs after handover. Some of that work:", "bullets": [{"fact_id": "client-facing-delivery", "title": "Client-Facing Delivery", "text": "At Turing I exceeded client KPIs for data accuracy and volume, helping take the team to #1 in dataset quality on client-verified benchmarks; at BoaSoft I shipped a RAG platform built around the client''s own documents."}, {"fact_id": "infrastructure-as-code", "title": "Infrastructure as Code", "text": "I design scalable AWS environments with Terraform and Docker, including a secure multi-tier VPC and modular application layers, so environments are reproducible across clients."}, {"fact_id": "gitops-secrets", "title": "GitOps & Secrets", "text": "I implement GitOps delivery with Argo CD, treating Git as the single source of truth for cluster state, and inject runtime credentials from HashiCorp Vault to keep secrets out of images and repositories."}], "provider": "none", "model": "deterministic", "grounded": true, "fallback_reason": null, "generated_at": "2026-10-11 06:03:30"}','restarted: first email only reached recruitment@virtualinfosecafrica.com','Sent','2026-10-07 00:00:00','2026-10-11 06:39:03');
INSERT INTO "companies" VALUES(87,'CyberHawk','https://www.cyber-hawk.com','cyber-hawk.com','consultancy','Accra, Ghana','local','ghana_based','https://www.cyber-hawk.com/','','Summary:

- What they do: CyberHawk provides cybersecurity solutions in Ghana, combining a strong local InfoSec team with Israeli and international experts to deliver managed security services and security risk mitigation for organizations.

- Products/services they build or offer:
  - Vulnerability Assessment and Penetration Testing (VAPT)
  - 24/7 managed security services (MSSPs), SOC-as-a-Service, SIEM-as-a-Service, endpoint and data protection
  - Incident response and security monitoring
  - Governance, risk, and compliance (GRC) solutions
  - Privileged Access Management (PAM)
  - Network security architecture and防 (prevention of unauthorized access, modification, denial of service)
  - Anti-fraud solutions (fraud prevention, detection, response)
  - Deception/decoy technologies for real-time attacker monitoring
  - Source code review to identify vulnerabilities and verify controls
  - Secure file transfer tools
  - Business continuity: Business Continuity Planning (BCP) and Disaster Recovery (DR)
  - Forensics services with chain-of-custody for admissible evidence
  - Training programs on cybersecurity best practices
  - Cloud-delivered solutions: SIEM, SOC, and related security services
  - Proprietary worldwide threat feed

- Who their customers are:
  - Organizations seeking comprehensive cybersecurity protection and risk management (various sectors). The emphasis is on enterprises needing 24/7 protection, threat detection/response, and regulatory compliance. Specific industries aren’t listed, but their services target businesses requiring managed security services, incident response, and compliance.

- Tech stack (inferred from offerings):
  - SIEM, SOC, and security monitoring platforms delivered as a service
  - Endpoint protection and data protection tooling
  - Cloud-delivered security services and threat intelligence feeds
  - Forensic and evidence-handling capabilities with chain-of-custody practices
  - Privileged Access Management systems
  - Deception/decoy technologies and vulnerability assessment tooling
  - Secure file transfer and code review tooling
  - BCP/DR tooling and procedures
  - Training platforms for staff cybersecurity education

If you want, I can tailor this to a specific industry (e.g., finance, telecom) or extract likely partners and competitive differentiators from their public materials.',NULL,'{"lead": "Client work rewards engineers who can drop into an unfamiliar setup and work out what the client actually needs. The harder part is leaving something that still runs after handover. Some of that work:", "bullets": [{"fact_id": "client-facing-delivery", "title": "Client-Facing Delivery", "text": "At Turing I exceeded client KPIs for data accuracy and volume, helping take the team to #1 in dataset quality on client-verified benchmarks; at BoaSoft I shipped a RAG platform built around the client''s own documents."}, {"fact_id": "infrastructure-as-code", "title": "Infrastructure as Code", "text": "I design scalable AWS environments with Terraform and Docker, including a secure multi-tier VPC and modular application layers, so environments are reproducible across clients."}, {"fact_id": "gitops-secrets", "title": "GitOps & Secrets", "text": "I implement GitOps delivery with Argo CD, treating Git as the single source of truth for cluster state, and inject runtime credentials from HashiCorp Vault to keep secrets out of images and repositories."}], "provider": "none", "model": "deterministic", "grounded": true, "fallback_reason": null, "generated_at": "2026-10-11 06:03:38"}','restarted: first email only reached info@cyber-hawk.com','Bounced','2026-10-07 00:00:00','2026-10-11 07:00:55');
INSERT INTO "companies" VALUES(88,'Kasazon Limited','https://www.kasazon.com','kasazon.com','consultancy','Accra, Ghana','local','ghana_based','https://www.kasazon.com/cybersecurity','',NULL,NULL,NULL,'generic_inbox_only','Pending','2026-10-07 00:00:00','2026-10-11 05:39:28');
INSERT INTO "companies" VALUES(89,'Boch Systems Ghana','https://www.bochsystems.net','bochsystems.net','consultancy','Accra, Ghana','local','ghana_based','https://www.bochsystems.net/pages/ghana.html','','Boch Systems is a cybersecurity and digital transformation advisory and services firm serving organizations across Africa (notably Ghana and Nigeria). What they do and offer:

- Core services:
  - Cybersecurity: 24/7 monitoring, threat detection, and incident response; security operations; security posture improvement.
  - Digital Transformation: modernizing infrastructure, applications, and processes for a future-ready organization.
  - VAPT & Assessments: vulnerability assessments and penetration testing.
  - Managed Security: ongoing monitoring and protection.
  - Cybersecurity awareness training: educating staff on security best practices.

- Approach and positioning:
  - Deep industry expertise with certified professionals.
  - Tailored, customer-centric solutions designed to solve unique challenges.
  - 24/7 support and monitoring for continuous protection.
  - Focus on measurable outcomes and business resilience.

- Notable outcomes and examples:
  - Strengthened security for a leading financial institution, reducing risk exposure (example outcome: 60% risk reduction from a robust security framework).
  - Emphasis on enabling secure digital transformation and resilient operations.
  - Proven track record with hundreds of projects and satisfied clients across industries.

- Customers: Public reference to “leading organizations across Africa and beyond,” with explicit mention of a major financial institution in their case highlights. They operate in Nigeria and Ghana and support institutions that require cybersecurity and digital modernization.

- Tech stack: The provided content does not specify concrete technologies or platforms (no listed products, tools, or vendor names). They emphasize AI-driven threat detection, cloud security and compliance, 24/7 SOC, and innovative solutions, but no explicit tech stack is disclosed.

In short: Boch Systems provides cybersecurity services, digital transformation consulting, and managed security, targeting enterprises (including financial institutions) in Africa with 24/7 monitoring and vulnerability assessments. They claim a strong track record and tailored, outcomes-focused engagements, but do not disclose their exact technology stack publicly.',NULL,'{"lead": "Client work rewards engineers who can drop into an unfamiliar setup and work out what the client actually needs. The harder part is leaving something that still runs after handover. Some of that work:", "bullets": [{"fact_id": "client-facing-delivery", "title": "Client-Facing Delivery", "text": "At Turing I exceeded client KPIs for data accuracy and volume, helping take the team to #1 in dataset quality on client-verified benchmarks; at BoaSoft I shipped a RAG platform built around the client''s own documents."}, {"fact_id": "infrastructure-as-code", "title": "Infrastructure as Code", "text": "I design scalable AWS environments with Terraform and Docker, including a secure multi-tier VPC and modular application layers, so environments are reproducible across clients."}, {"fact_id": "gitops-secrets", "title": "GitOps & Secrets", "text": "I implement GitOps delivery with Argo CD, treating Git as the single source of truth for cluster state, and inject runtime credentials from HashiCorp Vault to keep secrets out of images and repositories."}], "provider": "none", "model": "deterministic", "grounded": true, "fallback_reason": null, "generated_at": "2026-10-11 06:03:43"}',NULL,'Sent','2026-10-07 00:00:00','2026-10-11 06:41:01');
INSERT INTO "companies" VALUES(90,'OOSEC','https://oosecgh.com','oosecgh.com','consultancy','Accra, Ghana','local','ghana_based','https://oosecgh.com/about/','',NULL,NULL,NULL,NULL,'Pending','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(91,'SLAMM Technologies','https://www.slammghana.com','slammghana.com','consultancy','Accra, Ghana','local','ghana_based','https://www.slammghana.com/','',NULL,NULL,NULL,NULL,'Pending','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(92,'Kronix Shield','https://kronixshield.com','kronixshield.com','consultancy','Accra, Ghana','local','ghana_based','https://kronixshield.com/','',NULL,NULL,NULL,'people_found_no_email','Pending','2026-10-07 00:00:00','2026-10-11 05:39:28');
INSERT INTO "companies" VALUES(93,'VAS Cyber','https://vascyber.com','vascyber.com','consultancy','Accra, Ghana','local','ghana_based','https://vascyber.com/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(94,'Cybershield','https://www.cybershield.com.gh','cybershield.com.gh','consultancy','Accra, Ghana','local','ghana_based','https://www.cybershield.com.gh/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(95,'Lunar Tribe','https://www.lunartribe.tech','lunartribe.tech','consultancy','Accra, Ghana','local','ghana_based','https://www.lunartribe.tech/','',NULL,NULL,NULL,NULL,'Pending','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(96,'BigData Ghana','https://bigdataghana.com','bigdataghana.com','consultancy','Accra, Ghana','local','ghana_based','https://bigdataghana.com/','','Summary:

- What they do: BigData Ghana (BDG) is a Ghana-based GIS and geospatial intelligence company that converts geography, climate, and infrastructure data into decision-ready insights to help clients plan, build, invest, and operate with confidence. They focus on risk assessment, optimization, and growth planning using geospatial analysis.

- Products/services they build:
  - Geospatial intelligence and advanced GIS mapping/spatial analysis to reveal actionable insights (e.g., climate, infrastructure, operational risk).
  - Cloud and data platforms: design, build, and manage cloud and data infrastructures to scale data capabilities.
  - Data-enabled decision support: turning raw data into competitive decisions; data visualization and analytics for visibility, efficiency, and performance.
  - Enterprise Solutions (ERP): integrated systems for finance, HR, inventory, and operations to streamline processes.
  - Specific applications include flood modeling, yield prediction, real-time logistics, and national-scale spatial platforms.

- Customers (types): Organizations seeking risk assessment, planning, and optimization across sectors (construction/build, infrastructure, logistics, finance, government/municipal planning, and enterprises needing ERP and data platforms). They position themselves as serving businesses and public sector needs in Ghana with geospatial intelligence.

- Tech stack (inferred from offerings):
  - Geospatial/GIS analytics and mapping tools (likely GIS software and spatial analysis capabilities).
  - Cloud platforms and data engineering: cloud infrastructure design, data platforms, and scalable analytics.
  - Data analytics, AI: cloud/AI-enabled analytics to extract insight from data.
  - ERP systems for integrated finance, HR, and operations (enterprise software capabilities).
  - Specialized models: flood modeling, yield prediction, real-time logistics, and national-scale spatial platforms.

If you want, I can tailor this to a specific use case (e.g., for a construction firm evaluating site risk, or a logistics company exploring real-time routing).',NULL,'{"lead": "Client work rewards engineers who can drop into an unfamiliar setup and work out what the client actually needs. The harder part is leaving something that still runs after handover. Some of that work:", "bullets": [{"fact_id": "client-facing-delivery", "title": "Client-Facing Delivery", "text": "At Turing I exceeded client KPIs for data accuracy and volume, helping take the team to #1 in dataset quality on client-verified benchmarks; at BoaSoft I shipped a RAG platform built around the client''s own documents."}, {"fact_id": "infrastructure-as-code", "title": "Infrastructure as Code", "text": "I design scalable AWS environments with Terraform and Docker, including a secure multi-tier VPC and modular application layers, so environments are reproducible across clients."}, {"fact_id": "gitops-secrets", "title": "GitOps & Secrets", "text": "I implement GitOps delivery with Argo CD, treating Git as the single source of truth for cluster state, and inject runtime credentials from HashiCorp Vault to keep secrets out of images and repositories."}], "provider": "none", "model": "deterministic", "grounded": true, "fallback_reason": null, "generated_at": "2026-10-15 07:47:24"}',NULL,'Sent','2026-10-07 00:00:00','2026-10-15 07:48:19');
INSERT INTO "companies" VALUES(97,'Beron Intelligence','https://beronintelligence.com','beronintelligence.com','consultancy','Accra, Ghana','local','ghana_based','https://beronintelligence.com/','',NULL,NULL,NULL,'people_found_no_email','Pending','2026-10-07 00:00:00','2026-10-11 05:39:28');
INSERT INTO "companies" VALUES(98,'Codigits','https://codigits.com','codigits.com','consultancy','Accra, Ghana','local','ghana_based','https://codigits.com/data-analytics/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(99,'Mogital Analytics','https://www.mogitalanalytics.com','mogitalanalytics.com','ai','Accra, Ghana','local','ghana_based','https://www.mogitalanalytics.com/','',NULL,NULL,NULL,'people_found_no_email','Pending','2026-10-07 00:00:00','2026-10-11 05:39:28');
INSERT INTO "companies" VALUES(100,'DataMonk','https://datamonkapp.com','datamonkapp.com','general_startup','Accra, Ghana','local','ghana_based','https://datamonkapp.com/','',NULL,NULL,NULL,'people_found_no_email','Pending','2026-10-07 00:00:00','2026-10-11 05:39:28');
INSERT INTO "companies" VALUES(101,'Assets Circle Network Ltd','https://acnghana.com','acnghana.com','general_startup','Accra, Ghana','local','ghana_based','https://acnghana.com/','',NULL,NULL,NULL,'generic_inbox_only','Pending','2026-10-07 00:00:00','2026-10-11 05:39:28');
INSERT INTO "companies" VALUES(102,'Figtech','https://myfigtech.com','myfigtech.com','fintech','Accra, Ghana','local','ghana_based','https://myfigtech.com/about','','Summary:

- What the company does: MyFig is a fintech platform that positions life insurance as a vehicle for wealth building. It emphasizes transparency and optimization of life insurance policies to serve as a foundation for customers’ financial futures.

- Products/services they build: A system to track, compare, and optimize life insurance policies. The offering appears to combine policy management with tools to analyze and optimize insurance products for wealth-building goals (likely dashboards, comparisons, and optimization guidance).

- Who their customers are: Individuals seeking to use life insurance not only for protection but as an investment/wealth-building component. Likely targeted at financially conscious consumers who want transparency and optimization across their policies.

- Tech stack: The provided materials do not specify their technology stack. No details about programming languages, frameworks, or platforms are disclosed on the page.',NULL,'{"lead": "Payment systems don''t get to be flaky. Every transaction has to be reliable and auditable, and every release disciplined. Relevant work:", "bullets": [{"fact_id": "event-driven-financial-systems", "title": "Event-Driven Financial Systems", "text": "I won 1st place at the KNUST Technology Week Hackathon with a containerized remittance platform using Kafka for event streaming, a secure API gateway, an ACID-compliant orchestrator, and immutable audit logging."}, {"fact_id": "secure-cicd", "title": "Secure CI/CD", "text": "I engineered a cost-optimized Jenkins pipeline with auto-scaling EC2 Spot agents, and secured a Jenkins setup for 10 developers with Keycloak SSO and RBAC across 5 cross-functional teams."}, {"fact_id": "observability-mttr", "title": "Observability", "text": "I deployed Prometheus, Thanos, Loki, Grafana, and Jaeger with distributed tracing and automated alerting, reducing Mean Time To Resolution (MTTR)."}], "provider": "none", "model": "deterministic", "grounded": true, "fallback_reason": null, "generated_at": "2026-10-11 06:03:47"}',NULL,'Sent','2026-10-07 00:00:00','2026-10-11 06:41:55');
INSERT INTO "companies" VALUES(103,'Daabo','https://www.getdaabo.com','getdaabo.com','fintech','Accra, Ghana','local','ghana_based','https://www.getdaabo.com/about','','Daabo is an all-in-one insurance operations platform that digitizes and connects the end-to-end insurance lifecycle. It provides tools to create, price, quote, issue, manage, and renew insurance policies and add-ons, while embedding lead generation, routing, and customer support.

What they build (products/services)
- Centralized insurance service management: rate and price engines, add-ons, real-time premium tracking, secure data handling.
- Lead generation and compliance: multi-channel lead capture, smart scoring, auto-routing, SLA tracking, attribution/ROI analytics.
- Service builder and agent tools: e-policy issuance, claims handling, billing, renewals automation; onboarding/KYC verification; training, compliance tracking; agent mobile app with quotes, e-sign, premium collection.
- Integrations and ecosystem: connects with payment gateways, CRMs, KYC providers; omnichannel ticketing and AI chatbot; self-service client portal; secure data management.
- End-to-end scenarios: supports a full journey from quote to renewal with automated workflows, SLA timers, and real-time dashboards.

Who their customers are
- Insurance carriers and agencies seeking to streamline operations, quoting, policy issuance, claims, renewals, and compliance.
- Notable mentions include Meridian Insurance and other insurance leaders cited as users (via testimonials).

What tech stack or capabilities implied
- Cloud-based, single-platform integration across multiple services (quoting, rating, policy/claims management, CRM, payments, KYC, and mobile app).
- Real-time lead scoring, smart routing with SLA enforcement, attribution/ROI analytics.
- Digital policy lifecycle with add-ons and cost libraries, real-time premium tracking.
- Secure data management and e-signature capabilities via a mobile app for agents and self-service portals for customers.

Bottom line: Daabo offers a unified platform to create and price digital insurance services, generate and route leads, issue and manage policies/claims, and support customers via omnichannel tools, with real-time analytics and agent/mobile capabilities.',NULL,'{"lead": "Payment systems don''t get to be flaky. Every transaction has to be reliable and auditable, and every release disciplined. Relevant work:", "bullets": [{"fact_id": "event-driven-financial-systems", "title": "Event-Driven Financial Systems", "text": "I won 1st place at the KNUST Technology Week Hackathon with a containerized remittance platform using Kafka for event streaming, a secure API gateway, an ACID-compliant orchestrator, and immutable audit logging."}, {"fact_id": "secure-cicd", "title": "Secure CI/CD", "text": "I engineered a cost-optimized Jenkins pipeline with auto-scaling EC2 Spot agents, and secured a Jenkins setup for 10 developers with Keycloak SSO and RBAC across 5 cross-functional teams."}, {"fact_id": "observability-mttr", "title": "Observability", "text": "I deployed Prometheus, Thanos, Loki, Grafana, and Jaeger with distributed tracing and automated alerting, reducing Mean Time To Resolution (MTTR)."}], "provider": "none", "model": "deterministic", "grounded": true, "fallback_reason": null, "generated_at": "2026-10-11 06:03:53"}',NULL,'Sent','2026-10-07 00:00:00','2026-10-11 06:42:46');
INSERT INTO "companies" VALUES(104,'Maya','https://www.ridewithmaya.com','ridewithmaya.com','general_startup','Accra, Ghana','local','ghana_based','https://www.ridewithmaya.com/about-maya','','Summary:

- What the company does: Maya is a virtual assistant for car insurance. It enables users to buy, renew, and file claims for motor insurance through a chatbot interface, primarily via WhatsApp. It connects users with preferred insurers and aggregates quotes from multiple providers.

- Products/services they build: 
  - Short-term and future motor insurance policies with instant access
  - Policy management (buy, renew, file claims)
  - Flexible payment options (mobile money, Visa/Mastercard)
  - Direct claims filing to insurers via the platform (WhatsApp)
  - Instant delivery of policy documents and motor insurance stickers upon payment
  - Policy comparisons/quotes from multiple insurers
  - Agency/broker support (agents/brokers can connect to insurers and tie transactions to their customers)
  - Accessibility across devices (manage policies anytime, anywhere)

- Customers (target audience):
  - Individual vehicle owners seeking car insurance
  - Prospective buyers looking for multiple quotes from listed insurers
  - Agents or brokers who want to insure/renew/claim on behalf of clients
  - Anyone who prefers WhatsApp-based, chat-assisted insurance management

- Tech stack details (inferred from offerings):
  - Chatbot/Conversational AI layer (WhatsApp-based) for onboarding, quotes, buying, renewing, and claims
  - Backend integrations with multiple insurers to bind policies, renewals, and claims
  - Payment gateway integrations (mobile money, card payments)
  - Instant document delivery (policy certificates, stickers) via messaging (WhatsApp) and email
  - Multi-insurer quote aggregation and policy management workflow
  - Agent/broker authentication and transaction linking

Notes:
- The site emphasizes ease of use (under 5 minutes), WhatsApp-based claims filing, and direct insurer connections.
- No external links or image data were provided beyond the highlights.',NULL,'{"lead": "Startups need to ship fast without the platform falling over. Automating the slow, error-prone parts is how I make both possible:", "bullets": [{"fact_id": "infrastructure-velocity", "title": "Infrastructure Velocity", "text": "I provision production-ready AWS infrastructure with Terraform and Docker, including a secure multi-tier VPC and modular application layers."}, {"fact_id": "fast-feedback-loops", "title": "Fast Feedback Loops", "text": "I built a cost-optimized Jenkins CI/CD engine with EC2 Spot agents that auto-scale with build queue depth, speeding up developer feedback while cutting compute cost."}, {"fact_id": "developer-self-service", "title": "Developer Self-Service", "text": "I deployed Prometheus, Loki, Grafana, and Jaeger with self-service dashboards that give developers on-demand insight into their environments and error logs."}], "provider": "none", "model": "deterministic", "grounded": true, "fallback_reason": null, "generated_at": "2026-10-11 06:03:58"}',NULL,'Sent','2026-10-07 00:00:00','2026-10-11 06:43:21');
INSERT INTO "companies" VALUES(105,'wonfliki','https://wonfliki.com','wonfliki.com','general_startup','Accra, Ghana','local','ghana_based','https://wonfliki.com/','',NULL,NULL,NULL,'people_found_no_email','Pending','2026-10-07 00:00:00','2026-10-11 05:39:28');
INSERT INTO "companies" VALUES(106,'Complete Farmer','https://www.completefarmer.com','completefarmer.com','general_startup','Accra, Ghana','local','ghana_based','https://www.completefarmer.com/','','Summary:

What the company does
- A connected, data-driven platform for agriculture that unifies farmers, buyers, and vendors on one system. It enables end-to-end farming—from planning and securing inputs to farming management and market access—across West Africa, with global buyers available.

Products and services built
- Farm planning and remote farm management tools (plan, secure quality inputs, manage farm from anywhere).
- Digital marketplace for inputs, services, and tools sold to farmers.
- Sourcing and supply chain features for high-quality, export-ready produce with traceability and reliable sourcing.
- Data-driven insights and analytics to improve yields and profits.
- Access to a network and marketplace capabilities that connect farmers with thousands of active buyers (global agro-commodity buyers).

Customers
- Farmers (including thousands of real growers in Ghana and West Africa) who access inputs, services, and data-driven insights.
- Global/exports-ready buyers looking to source West African produce.
- Vendors and suppliers selling agricultural inputs and tools on the platform.

What tech stack is used
- The page does not specify the exact technology stack (no details on languages, frameworks, hosting, or architecture). It emphasizes a connected, data-driven platform with marketplace, marketplace logistics, traceability, and analytics features, but no explicit tech stack is disclosed.

Key takeaways
- One platform integrating farming, inputs, marketplace, and buyers to streamline agriculture in West Africa.
- Enables planning, sourcing, farming management, and access to a global buyer network.
- Focus on traceability and reliable sourcing with a digital marketplace for inputs and services.',NULL,'{"lead": "Startups need to ship fast without the platform falling over. Automating the slow, error-prone parts is how I make both possible:", "bullets": [{"fact_id": "infrastructure-velocity", "title": "Infrastructure Velocity", "text": "I provision production-ready AWS infrastructure with Terraform and Docker, including a secure multi-tier VPC and modular application layers."}, {"fact_id": "fast-feedback-loops", "title": "Fast Feedback Loops", "text": "I built a cost-optimized Jenkins CI/CD engine with EC2 Spot agents that auto-scale with build queue depth, speeding up developer feedback while cutting compute cost."}, {"fact_id": "developer-self-service", "title": "Developer Self-Service", "text": "I deployed Prometheus, Loki, Grafana, and Jaeger with self-service dashboards that give developers on-demand insight into their environments and error logs."}], "provider": "none", "model": "deterministic", "grounded": true, "fallback_reason": null, "generated_at": "2026-10-11 06:04:03"}',NULL,'Sent','2026-10-07 00:00:00','2026-10-11 06:44:04');
INSERT INTO "companies" VALUES(107,'Farmerline','http://farmerline.co','farmerline.co','ai','Accra, Ghana','local','ghana_based','https://justfarm.ai/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(108,'AGRISAT TECHNOLOGY','https://www.agrisattechnologies.com','agrisattechnologies.com','fintech','Accra, Ghana','local','ghana_based','https://www.agrisattechnologies.com/','',NULL,NULL,NULL,NULL,'Pending','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(109,'Sesi Technologies','https://sesitechnologies.com','sesitechnologies.com','general_startup','Accra, Ghana','local','ghana_based','https://sesitechnologies.com/','','Sesi Technologies is a Ghana-based tech-enabled agribusiness focused on boosting productivity and income for African farmers and agribusinesses. They build and provide end-to-end, locally designed technologies and services to reduce post-harvest losses, improve storage and market access, and enable data-driven farming.

What they do and the products/services they offer:
- Post-harvest solutions for smallholder grain farmers: a suite of post-harvest technologies, mechanization services, and market access to reduce losses and raise income.
- For agribusiness and processing: technologies to measure grain moisture, reduce storage losses, and boost productivity.
- Digital marketplace: connects grain aggregators, traders, and suppliers to new markets and partners.
- FarmSense soil intelligence platform: hardware, software, and AI-based soil testing and insights to help farmers and agribusinesses optimize yields.
- GrainMate moisture measurement: handheld moisture meter to ensure grains are dry enough for storage.
- GrainMate Warehouse Monitor: monitoring of warehouse temperature and humidity with mobile-accessible intelligent climate reports.
- ZeroFly Hermetic Storage Bags: hermetic bags protecting stored grains/seeds from internal and external pests.

Who their customers are:
- Smallholder farmers and agribusinesses (agribusinesses, commodity traders, aggregators, feed producers, and food processing companies).
- Grain traders and storage facilities that need moisture control and climate monitoring.
- Farmers and agribusinesses seeking soil insights and data-driven decisions.

Tech stack (explicit details limited in the provided content):
- FarmSense platform: combines hardware, software, and AI for soil intelligence (no specific technologies listed).
- GrainMate products: hardware tools (moisture meter and warehouse monitor) with a supporting app for data access and reporting.
- Hermetic storage bags: physical product technology with hermetic inner layer for pest protection.
- Digital marketplace: software platform to connect aggregators/traders with markets and suppliers.
Note: The exact technical stack (programming languages, cloud providers, data platforms, etc.) is not specified in the provided materials.

In short, Sesi Technologies builds affordable, locally designed hardware/software solutions for soil health, moisture and storage monitoring, post-harvest handling, and marketplace access, targeting smallholder farmers and agribusiness entities in Africa.',NULL,'{"lead": "Startups need to ship fast without the platform falling over. Automating the slow, error-prone parts is how I make both possible:", "bullets": [{"fact_id": "infrastructure-velocity", "title": "Infrastructure Velocity", "text": "I provision production-ready AWS infrastructure with Terraform and Docker, including a secure multi-tier VPC and modular application layers."}, {"fact_id": "fast-feedback-loops", "title": "Fast Feedback Loops", "text": "I built a cost-optimized Jenkins CI/CD engine with EC2 Spot agents that auto-scale with build queue depth, speeding up developer feedback while cutting compute cost."}, {"fact_id": "developer-self-service", "title": "Developer Self-Service", "text": "I deployed Prometheus, Loki, Grafana, and Jaeger with self-service dashboards that give developers on-demand insight into their environments and error logs."}], "provider": "none", "model": "deterministic", "grounded": true, "fallback_reason": null, "generated_at": "2026-10-15 07:47:02"}',NULL,'Sent','2026-10-07 00:00:00','2026-10-15 07:48:58');
INSERT INTO "companies" VALUES(110,'Alster Limited','https://alstergh.com','alstergh.com','consultancy','Accra, Ghana','local','ghana_based','https://alstergh.com/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(111,'Zerol Limited','https://www.zerolafrica.com','zerolafrica.com','general_startup','Accra, Ghana','local','ghana_based','https://www.zerolafrica.com/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(112,'XCelerate AK','https://xcelerateak.com','xcelerateak.com','ai','Accra, Ghana','local','ghana_based','https://xcelerateak.com/','',NULL,NULL,NULL,'people_found_no_email','Pending','2026-10-07 00:00:00','2026-10-11 05:39:28');
INSERT INTO "companies" VALUES(113,'Modularpath','https://modularpath.dev','modularpath.dev','general_startup','Accra, Ghana','local','ghana_based','https://modularpath.dev/','',NULL,NULL,NULL,'people_found_no_email','Pending','2026-10-07 00:00:00','2026-10-11 05:39:28');
INSERT INTO "companies" VALUES(114,'OddHaus Digital','https://www.oddhaus.com','oddhaus.com','consultancy','Accra, Ghana','local','ghana_based','https://www.oddhaus.com/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(115,'CleverTech Studio','https://www.clevertech.studio','clevertech.studio','ai','Accra, Ghana','local','ghana_based','https://www.clevertech.studio/','',NULL,NULL,NULL,'generic_inbox_only','Pending','2026-10-07 00:00:00','2026-10-11 05:39:28');
INSERT INTO "companies" VALUES(116,'Akanexus','https://akanexus.com','akanexus.com','consultancy','Accra, Ghana','local','ghana_based','https://akanexus.com/','',NULL,NULL,NULL,'generic_inbox_only','Pending','2026-10-07 00:00:00','2026-10-11 05:39:28');
INSERT INTO "companies" VALUES(117,'Abeyie Innovation Studios','https://abeyiestudios.com','abeyiestudios.com','consultancy','Accra, Ghana','local','ghana_based','https://abeyiestudios.com/','','Abeyie Innovation Studios is a multi-disciplinary innovation firm focused on helping organizations modernize and thrive through technology, design, and strategic programs. Key offerings and focus:

- Core services
  - Innovation Consulting: digital transformation, automation, software development, product strategy, and platform-enabled modernization.
  - Branding & Creative Engineering: brand design, visual systems, product experiences, and communication assets.
  - Leadership & Coaching: leadership development, governance advisory, and organizational capacity building.
  - Insights & Future Intelligence: building a long-term knowledge and insights engine for decision-making.

- What they build (products/services)
  - Digital platforms, management systems, mobile apps, custom software
  - Workflow automation tools and other digital enablement solutions
  - Creative experiences and strategic structures to support ecosystem growth

- Customers / target audiences
  - SMEs and corporates
  - Startups and founders
  - Women-led ventures
  - Non-profits and social impact organizations
  - Educational institutions
  - Executive leaders and professionals
  - Policy and development organizations

- Partnerships and collaborators
  - Public and private partners via innovation programs, leadership development, product co-creation, research/policy projects, and digital transformation initiatives
  - International collaboration with global tech players (notably Microsoft, Google, IBM)

- Tech stack specifics
  - The site and highlights emphasize capabilities in software development, digital platforms, automation, and ecosystem platforms, but do not list concrete technologies (programming languages, frameworks, or tools) in the provided content.

- Distinguishing notes
  - They have support and collaboration from major global tech funders and operate across multiple sectors including entrepreneurship, leadership, digital transformation, product innovation, and ecosystem building.
  - They position themselves as building systems and platforms to power Africa’s next generation of organizations and entrepreneurs.

If you need, I can tailor this to a specific aspect (e.g., potential partnership angles, client types, or confirm any explicit tech stack if you have more detailed materials).',NULL,'{"lead": "Client work rewards engineers who can drop into an unfamiliar setup and work out what the client actually needs. The harder part is leaving something that still runs after handover. Some of that work:", "bullets": [{"fact_id": "client-facing-delivery", "title": "Client-Facing Delivery", "text": "At Turing I exceeded client KPIs for data accuracy and volume, helping take the team to #1 in dataset quality on client-verified benchmarks; at BoaSoft I shipped a RAG platform built around the client''s own documents."}, {"fact_id": "infrastructure-as-code", "title": "Infrastructure as Code", "text": "I design scalable AWS environments with Terraform and Docker, including a secure multi-tier VPC and modular application layers, so environments are reproducible across clients."}, {"fact_id": "gitops-secrets", "title": "GitOps & Secrets", "text": "I implement GitOps delivery with Argo CD, treating Git as the single source of truth for cluster state, and inject runtime credentials from HashiCorp Vault to keep secrets out of images and repositories."}], "provider": "none", "model": "deterministic", "grounded": true, "fallback_reason": null, "generated_at": "2026-10-11 06:04:09"}',NULL,'Bounced','2026-10-07 00:00:00','2026-10-11 07:00:56');
INSERT INTO "companies" VALUES(118,'OhWP Studios','https://ohwpstudios.online','ohwpstudios.online','consultancy','Accra, Ghana','local','ghana_based','https://ohwpstudios.online/','',NULL,NULL,NULL,'no_contact_found','Skipped','2026-10-07 00:00:00','2026-10-10 12:24:58');
INSERT INTO "companies" VALUES(119,'4th-IR','https://www.4th-ir.com','4th-ir.com','ai','Accra, Ghana','local','ghana_based','https://www.4th-ir.com/about-us','https://www.linkedin.com/company/4th-ir/jobs/','Summary:
4th-IR is a services-focused AI and digital transformation firm that helps businesses navigate the 4th Industrial Revolution. They turn AI-driven ideas into deployable solutions using their platform Twynity and a network of experts and virtual resources. They offer AI-powered, customizable virtual tools and assistants to streamline operations across industries such as healthcare, finance, and public sector.

What they build and offer:
- Twynity platform: enables ideation to deployment of AI solutions; supports building tailored virtual assistants and AI applications.
- AI-powered virtual resources and tools, including:
  - Virtual Screening Assistant: AI-driven candidate screening and recommendations.
  - Virtual Migration Tool: AI-assisted data migration with validation, enrichment, and transformation.
  - Virtual Compliance Officer: AI-driven regulatory understanding for compliance.
  - Frank Chatbot: Regulatory chatbot for a public health organization.
- Industry-focused applications:
  - Healthcare data ingestion, analysis, and visualization for hospital networks.
  - Regulatory and compliance automation for health and public sectors.
  - Automated ticket analysis for financial institutions.
  - Access to funding for quality healthcare across Africa.

Customers:
- Public health and regulatory bodies (Germany, public health organizations).
- Healthcare providers (hospital chains, Africa-focused healthcare access initiatives).
- Financial institutions (Germany) seeking automated ticket analysis.
- Organizations seeking AI-driven virtual assistants and streamlined operations across healthcare, finance, and public sectors.

What tech stack or capabilities they use (inferred from content):
- AI-driven automation and platform-based development (Twynity) for building virtual assistants and AI solutions.
- Natural language processing / chatbot capabilities (e.g., Frank Chatbot; Virtual Compliance Officer).
- Data engineering tooling for data ingestion, validation, enrichment, transformation (Virtual Migration Tool).
- AI-powered recruiting automation (Virtual Screening Assistant).
- Compliance-aware AI systems for regulatory understanding.

Note: The site emphasizes rapid, tailored AI solutions with expert guidance, leveraging a global talent pool and a structured 9-step methodology from ideation to deployment. No specific software stacks or vendors are listed.',NULL,'{"lead": "Getting AI out of a demo and into a customer''s hands is an engineering problem as much as a modelling one. I work on both halves:", "bullets": [{"fact_id": "applied-ai-delivery", "title": "Applied AI Delivery", "text": "I built an end-to-end RAG system with FastAPI and the Zilliz vector store, grounding answers in a client''s verified documents, with a serverless ingestion pipeline and a React frontend for context-aware document interrogation."}, {"fact_id": "evaluation-driven-agents", "title": "Evaluation-Driven Agents", "text": "I architected a natural-language analytics agent on CopilotKit and Cube Core, and used a DeepEval golden dataset to raise output reliability from 74% to 96% by constraining queries to declared measures and dimensions."}, {"fact_id": "production-platform", "title": "Production Platform", "text": "I run containerized workloads on production Kubernetes with GitOps delivery via Argo CD, secrets from HashiCorp Vault, and Prometheus, Loki, Grafana, and Jaeger observability, so what I ship stays running."}], "provider": "none", "model": "deterministic", "grounded": true, "fallback_reason": null, "generated_at": "2026-10-11 06:04:31"}','restarted: first email only reached info@4th-ir.com','Sent','2026-10-07 00:00:00','2026-10-11 06:45:27');
INSERT INTO "companies" VALUES(120,'Bridgeway Technology Limited','https://bridgewaytec.com','bridgewaytec.com','fintech','Accra, Ghana','local','ghana_based','https://bridgewaytec.com/company/careers/fintech-platform-engineer','',NULL,NULL,NULL,NULL,'Pending','2026-10-15 07:02:34','2026-10-15 07:02:34');
INSERT INTO "companies" VALUES(121,'Hurain Technologies','https://www.huraintechnologies.com','huraintechnologies.com','consultancy','Accra, Ghana','local','ghana_based','https://www.huraintechnologies.com/industries/banking-fintech/ghana/accra','',NULL,NULL,NULL,'people_found_no_email','Pending','2026-10-15 07:02:37','2026-10-15 07:05:53');
INSERT INTO "companies" VALUES(122,'Zethic','https://zethic.com','zethic.com','consultancy','Accra, Ghana','local','ghana_based','https://zethic.com/industries/financial-services/fintech-software-development-accra/','','Summary:

- What the company does: Zethic provides AI-first digital solutions and end-to-end software engineering services. They embed AI into the core of systems (not as a bolt‑on) and offer a full spectrum from strategy to scale, including architecture, development, integration, and ongoing managed services.

- Products/services they build: 
  - AI Development and AI Workflow Automation
  - Agentic AI Development
  - AI Consult & Audit
  - Machine Learning Development
  - Digital Transformation and Legacy Software Modernization
  - Custom Application Development
  - Data Engineering and typed APIs, secure deployment pipelines
  - Rebuilding/Rescuing legacy systems (security, scalability, modern tech stacks)
  - End-to-end solutions for Banking (fraud detection, automated KYC, core banking), Insurance, and Transport/Logistics (route optimization, demand forecasting, real-time visibility)
  - Management of IT/Cloud services and fractional CTO partnerships
  - Design and product discovery (design audits, prototypes, UX)
  - Marketing creative and usability enhancements

- Ideal customers: SME to mid-market organizations in regulated or complex sectors needing scalable AI-enabled platforms and modern software architectures. They mention banking, insurance, and logistics as example verticals, but position as partners for organizations with legacy systems needing modernization or AI integration.

- Tech stack and approach:
  - AI integrated into foundation: typed APIs, trusted data pipelines, robust deployment infra
  - End-to-end engineering with senior-led teams
  - Focus on sustainable, scalable architecture, security posture, and maintainable code
  - CI/CD pipelines, security reviews, rigorous QA, and clear documentation
  - “Rescue or fresh build” model: rearchitect/modernize existing systems or build new from scratch with long-term maintainability
  - Managed IT/Cloud services and fractional CTO offerings to sustain growth post-launch

If you want, I can tailor this to your specific area (e.g., banking, logistics) or map it to their exact service lines with a quick bullets-to-pitches conversion.',NULL,'{"lead": "Client work rewards engineers who can drop into an unfamiliar setup and work out what the client actually needs. The harder part is leaving something that still runs after handover. Some of that work:", "bullets": [{"fact_id": "client-facing-delivery", "title": "Client-Facing Delivery", "text": "At Turing I exceeded client KPIs for data accuracy and volume, helping take the team to #1 in dataset quality on client-verified benchmarks; at BoaSoft I shipped a RAG platform built around the client''s own documents."}, {"fact_id": "infrastructure-as-code", "title": "Infrastructure as Code", "text": "I design scalable AWS environments with Terraform and Docker, including a secure multi-tier VPC and modular application layers, so environments are reproducible across clients."}, {"fact_id": "gitops-secrets", "title": "GitOps & Secrets", "text": "I implement GitOps delivery with Argo CD, treating Git as the single source of truth for cluster state, and inject runtime credentials from HashiCorp Vault to keep secrets out of images and repositories."}], "provider": "none", "model": "deterministic", "grounded": true, "fallback_reason": null, "generated_at": "2026-10-15 07:06:57"}',NULL,'Sent','2026-10-15 07:02:39','2026-10-15 07:09:03');
INSERT INTO "companies" VALUES(123,'expressPay Ghana','https://expresspaygh.com','expresspaygh.com','fintech','Accra, Ghana','local','ghana_based','https://ghanajobsearch.com/job/senior-fintech-software-engineer-opportunity-in-accra/','','expressPay is a payment technology company that provides API-driven and merchant-focused payment solutions aimed at enabling businesses to accept and manage payments across multiple channels. Key offerings include:

What they do
- Provide API integration for seamless card and mobile money payments across platforms.
- Enable contactless payments via QR codes and QR decals for quick in-person transactions.
- Bill payment services for banks, utilities, and other providers to bill customers and collect payments.
- Android POS devices capable of initiating/accepting mobile money payments, NFC payments (mobile and NFC-enabled cards), and traditional card payments.
- Bulk payment processing (file-based transactions) for paying many suppliers with a single click.
- USSD payment solutions compatible with all mobile networks.
- P2P transfers (send money to friends/family/bank accounts).
- Mobile top-ups and internet bundles.

Who their customers are
- Merchants and businesses needing multi-channel payment acceptance (in-store via QR, POS, NFC, and cards).
- Banks and utility/service providers requiring bill pay capabilities.
- Companies that process bulk supplier payments and need efficient reconciliation.
- Consumers who want quick payments, top-ups, and transfers.

What products/services they build
- Payment acceptance API (cards and mobile money).
- QR-based contactless payment system (QR decals for merchants).
- Bill payment services for institutions.
- Android POS devices with support for mobile money, NFC, and card payments.
- Bulk payments/file-based processing.
- USSD payment solutions.
- P2P transfers and mobile top-up services.

Technology stack (inferred from offerings)
- API-first platform for payment integrations (likely RESTful APIs; could include webhooks).
- NFC and mobile payments support (likely secure element/NFC stack on devices).
- QR code generation and scanning infrastructure for merchant payments.
- USSD backend integration with mobile operators.
- PCI-DSS-compliant data handling (explicit PCI certification).
- Mobile/Android device software for POS functionality.
- Backend payment processing and settlement systems capable of bulk transactions.

Notes
- They emphasize PCI certification for data protection.
- Their solution suite targets merchants needing multi-channel payments, bill payments, bulk supplier payments, and consumer mobile money/top-up services.',NULL,'{"lead": "Payment systems don''t get to be flaky. Every transaction has to be reliable and auditable, and every release disciplined. Relevant work:", "bullets": [{"fact_id": "event-driven-financial-systems", "title": "Event-Driven Financial Systems", "text": "I won 1st place at the KNUST Technology Week Hackathon with a containerized remittance platform using Kafka for event streaming, a secure API gateway, an ACID-compliant orchestrator, and immutable audit logging."}, {"fact_id": "secure-cicd", "title": "Secure CI/CD", "text": "I engineered a cost-optimized Jenkins pipeline with auto-scaling EC2 Spot agents, and secured a Jenkins setup for 10 developers with Keycloak SSO and RBAC across 5 cross-functional teams."}, {"fact_id": "observability-mttr", "title": "Observability", "text": "I deployed Prometheus, Thanos, Loki, Grafana, and Jaeger with distributed tracing and automated alerting, reducing Mean Time To Resolution (MTTR)."}], "provider": "none", "model": "deterministic", "grounded": true, "fallback_reason": null, "generated_at": "2026-10-15 07:07:02"}',NULL,'Sent','2026-10-15 07:02:40','2026-10-15 07:09:41');
INSERT INTO "companies" VALUES(124,'turntabl','https://turntabl.io','turntabl.io','consultancy','Accra, Ghana','local','ghana_based','https://turntabl.io/','','Turntabl builds senior-led software engineering teams in Accra for UK fintechs and financial institutions. Their model centers on long-running, embedded teams that stay with clients year after year, rather than one-off staff augmentation.

What they do / services:
- Engineering teams: end-to-end software delivery across architecture, development, testing, deployment, and operations.
- Agile software engineering: custom web, mobile, and enterprise apps embedded in clients’ sprints and codebases.
- Solutions architecture: system design for scale, auditability, and change.
- DevOps: CI/CD, infrastructure as code, monitoring for reliable releases.
- Quality assurance: automated test suites to prevent regressions.
- Enterprise data: data platforms and pipelines with scale, lineage, and regulatory compliance.
- Generative AI: taking LLM projects from prototype to production with evaluation and compliance built in.
- Research & design: rapid prototyping to validate directions before committing budget.
- Engineering strategy: delivery planning, hiring, and platform decisions aligned with teams on the ground.

Who their customers are:
- Fintechs and financial institutions in the UK and beyond, including tier-one financial services firms.
- Industries requiring high reliability under load, audit, and regulatory scrutiny (e.g., investment management, trading platforms, payments, retail banking, crypto/digital assets).

Key capabilities and positioning:
- Teams anchored by an Engineering Lead, integrated with clients’ tech leadership.
- Strong emphasis on long-term engagement: most engineers stay on client teams, and clients typically start with one team and expand.
- Accra-based delivery with near-UK-time overlap (within an hour), enabling a full overlapping workday.
- Deep fintech focus: low-latency, high-availability, and regulatory-compliant systems.
- R&D validation and a patent-pending dimensional data tool; active involvement in FINOS (Fintech Open Source Foundation).
- Training pipeline: over 1,000 engineers apply yearly; those who join complete a four-month Wall Street–standard training before client work.

Tech stack (inferred from services and fintech focus):
- Software engineering: web, mobile, and enterprise application development.
- Architecture and platform: scalable system design for regulated, high-availability contexts.
- DevOps and CI/CD: infrastructure as code, automated monitoring.
- Data: data platforms and pipelines with data lineage and regulatory considerations.
- AI/ML: generative AI/LLM applications with production-grade governance.
- Testing: automated QA and regression testing frameworks.
Note: Specific technologies (languages, frameworks, cloud providers) are not enumerated in the provided materials. Their emphasis is on robust, scalable, compliant fintech delivery rather than a fixed stack.',NULL,'{"lead": "Client work rewards engineers who can drop into an unfamiliar setup and work out what the client actually needs. The harder part is leaving something that still runs after handover. Some of that work:", "bullets": [{"fact_id": "client-facing-delivery", "title": "Client-Facing Delivery", "text": "At Turing I exceeded client KPIs for data accuracy and volume, helping take the team to #1 in dataset quality on client-verified benchmarks; at BoaSoft I shipped a RAG platform built around the client''s own documents."}, {"fact_id": "infrastructure-as-code", "title": "Infrastructure as Code", "text": "I design scalable AWS environments with Terraform and Docker, including a secure multi-tier VPC and modular application layers, so environments are reproducible across clients."}, {"fact_id": "gitops-secrets", "title": "GitOps & Secrets", "text": "I implement GitOps delivery with Argo CD, treating Git as the single source of truth for cluster state, and inject runtime credentials from HashiCorp Vault to keep secrets out of images and repositories."}], "provider": "none", "model": "deterministic", "grounded": true, "fallback_reason": null, "generated_at": "2026-10-15 07:07:07"}',NULL,'Sent','2026-10-15 07:02:42','2026-10-15 07:10:21');
INSERT INTO "companies" VALUES(125,'DIREKTDOTCOM','https://direktdot.com','direktdot.com','consultancy','Accra, Ghana','local','ghana_based','https://direktdot.com/en/services/web-application-development-in-accra','',NULL,NULL,NULL,'generic_inbox_only','Pending','2026-10-15 07:02:43','2026-10-15 07:06:36');
INSERT INTO "companies" VALUES(126,'Oyster','https://oysterhr.com','oysterhr.com','general_startup','','remote','worldwide','https://jobs.ashbyhq.com/oyster','https://www.oysterhr.com/careers','Oyster HR is an employer-of-record (EOR) and global payroll platform that lets companies hire, pay, and manage employees and contractors in 180+ countries without establishing local entities. Key offerings include compliant onboarding (as fast as 48 hours), payroll, benefits administration, and HR support, with integrations to HRIS, ATS, and accounting systems. They position themselves as human-centric with transparent pricing and operate as a certified B Corp.

Products/services:
- Global EOR: hire, onboard, payroll, benefits across 180+ countries without local entities
- Global contractors: compliant contractor management and payroll
- People services: white-glove HR advice and local expertise
- Integrations: connects with HRIS, ATS, and accounting systems
- Transparent, fixed pricing for predictable costs

Customers:
- Companies with international hiring needs, including fast-growing firms and engineering teams seeking global talent. They emphasize serving Britain, Ireland, and other markets, targeting teams that want compliant access to global talent quickly.

Tech stack (implied from offering):
- Cloud-based platform with automation for onboarding, payroll, benefits, and compliance
- Integrations with HRIS, ATS, and accounting systems
- No explicit stack details provided; focus is on EOR platform capabilities and global payroll tooling

If you want, I can tailor this to a specific use case (e.g., a hiring manager at a tech startup) or compare Oyster to other EOR providers.',NULL,'{"lead": "Startups need to ship fast without the platform falling over. Automating the slow, error-prone parts is how I make both possible:", "bullets": [{"fact_id": "infrastructure-velocity", "title": "Infrastructure Velocity", "text": "I provision production-ready AWS infrastructure with Terraform and Docker, including a secure multi-tier VPC and modular application layers."}, {"fact_id": "fast-feedback-loops", "title": "Fast Feedback Loops", "text": "I built a cost-optimized Jenkins CI/CD engine with EC2 Spot agents that auto-scale with build queue depth, speeding up developer feedback while cutting compute cost."}, {"fact_id": "developer-self-service", "title": "Developer Self-Service", "text": "I deployed Prometheus, Loki, Grafana, and Jaeger with self-service dashboards that give developers on-demand insight into their environments and error logs."}], "provider": "none", "model": "deterministic", "grounded": true, "fallback_reason": null, "generated_at": "2026-10-15 07:07:11"}',NULL,'Sent','2026-10-15 07:03:06','2026-10-15 07:15:02');
INSERT INTO "companies" VALUES(127,'Protocol Labs','https://protocol.ai','protocol.ai','general_startup','','remote','worldwide','https://protocol.ai/join/','https://protocol.ai/join/','Summary:

- What the company does: Protocol Labs is an innovation network and research- and product-focused organization that drives breakthroughs in computing to push humanity forward. It connects and supports a broad ecosystem (over 750 startups, funds, accelerators, foundations, open source projects, service providers, and other organizations). Its work spans web3, AI, AR/VR, hardware, and emerging technologies.

- Products/Services they build or support:
  - Core open-source projects originally: IPFS (InterPlanetary File System), Filecoin, and libp2p, with ongoing support and expansion.
  - Platform tools and connective tissue to enable collaboration and infrastructure for its ecosystem.
  - Focus areas and programs aroundDigital Human Rights, Economies and Governance (crypto, AI, programmable digital public infrastructure), AI and Robotics, and Neurotech (BCI, NeuroAI, Whole Brain Emulation).
  - Investment via PL Capital in venture-scale ideas.

- Customers/Users:
  - Tech startups, funds, accelerators, foundations, open source projects, service providers, and other ecosystem participants that rely on Protocol Labs infrastructure and funding.
  - Broadly targets developers and organizations building on decentralized infrastructure (IPFS/Filecoin/libp2p) and those exploring AI, robotics, neurotech, and Web3.

- Tech stack (publicly emphasized):
  - Foundational decentralized and distributed systems: IPFS, Filecoin, libp2p.
  - Web3, decentralized storage, and programmable public infrastructure.
  - AI, robotics, and neurotech components as areas of exploration and product/infra development.
  - Platform tooling and connective tissue to coordinate a large ecosystem (likely open-source, standards-based, interoperable components).

If you want, I can tailor this to a specific aspect (e.g., detailed product roadmap, customer personas, or a Tech Stack diagram) or pull in more concrete project examples.',NULL,'{"lead": "Startups need to ship fast without the platform falling over. Automating the slow, error-prone parts is how I make both possible:", "bullets": [{"fact_id": "infrastructure-velocity", "title": "Infrastructure Velocity", "text": "I provision production-ready AWS infrastructure with Terraform and Docker, including a secure multi-tier VPC and modular application layers."}, {"fact_id": "fast-feedback-loops", "title": "Fast Feedback Loops", "text": "I built a cost-optimized Jenkins CI/CD engine with EC2 Spot agents that auto-scale with build queue depth, speeding up developer feedback while cutting compute cost."}, {"fact_id": "developer-self-service", "title": "Developer Self-Service", "text": "I deployed Prometheus, Loki, Grafana, and Jaeger with self-service dashboards that give developers on-demand insight into their environments and error logs."}], "provider": "none", "model": "deterministic", "grounded": true, "fallback_reason": null, "generated_at": "2026-10-15 07:07:15"}',NULL,'Sent','2026-10-15 07:03:35','2026-10-15 07:12:32');
INSERT INTO "companies" VALUES(128,'WebSys Ghana Limited','https://www.facebook.com','facebook.com','consultancy','Ghana','local','ghana_based','https://www.businessghana.com/site/directory/software-development/it','',NULL,NULL,NULL,NULL,'Pending','2026-10-15 07:41:34','2026-10-15 07:41:34');
INSERT INTO "companies" VALUES(129,'Boost','https://www.withboost.co','withboost.co','general_startup','','remote','explicit_ghana','https://jobgether.com/offer/6aa858b8b563ea142ea8efe3-senior-backend-engineer','https://jobgether.com/offer/6aa858b8b563ea142ea8efe3-senior-backend-engineer','Boost is a B2B commerce platform focused on Africa’s convenience economy. It digitizes and scales wholesale and retail operations across multiple markets using a single, flexible platform.

What they do / products & services
- B2B commerce platform for distributors, suppliers, and new brands
- Effortless WhatsApp ordering to digitize demand
- Data-light apps for fulfilment and payments management
- Multi-language, multi-currency catalogues with channel- and territory-specific pricing
- Stock financing through Stock Boosts and real-time analytics with actionable reports
- On-the-ground onboarding and customer success teams in Egypt, Ghana, Kenya, and Nigeria
- Digital pre-ordering, promotions, retailer insights to increase market access and reduce costs

Who their customers are
- Distributors (digitizing manual processes, integrating order management for retailer networks)
- Suppliers (expanding market access and penetration via digital ordering and insights)
- New brands (access to distributor/retailer networks, technology, and data insights)

What’s notable about their technology / stack
- A single, scalable platform designed to serve multiple markets with localization (languages, currencies) and multiple catalogues/prices
- Support for channel-based and territory-based configurations
- WhatsApp-based ordering and data-light apps for ease of use in low-connectivity contexts
- Real-time analytics and reporting
- Stock financing integration (Stock Boosts) to unlock growth
- Local onboarding teams suggest a strong services/implementation layer complementing the platform

Key takeaway: Boost provides a scalable, localized B2B commerce platform for Africa’s retail/distribution networks, combining digital ordering, fulfilment, payments, analytics, and financing to help distributors, suppliers, and brands grow in the convenience economy. Interested in partnerships or investment opportunities.',NULL,'{"lead": "Startups need to ship fast without the platform falling over. Automating the slow, error-prone parts is how I make both possible:", "bullets": [{"fact_id": "infrastructure-velocity", "title": "Infrastructure Velocity", "text": "I provision production-ready AWS infrastructure with Terraform and Docker, including a secure multi-tier VPC and modular application layers."}, {"fact_id": "fast-feedback-loops", "title": "Fast Feedback Loops", "text": "I built a cost-optimized Jenkins CI/CD engine with EC2 Spot agents that auto-scale with build queue depth, speeding up developer feedback while cutting compute cost."}, {"fact_id": "developer-self-service", "title": "Developer Self-Service", "text": "I deployed Prometheus, Loki, Grafana, and Jaeger with self-service dashboards that give developers on-demand insight into their environments and error logs."}], "provider": "none", "model": "deterministic", "grounded": true, "fallback_reason": null, "generated_at": "2026-10-15 07:47:28"}',NULL,'Sent','2026-10-15 07:41:49','2026-10-15 07:50:02');
INSERT INTO "companies" VALUES(130,'Cosbyte','https://cosbyte.com','cosbyte.com','general_startup','','remote','explicit_ghana','https://cosbyte.com/job-fullstack.html','https://cosbyte.com/job-fullstack.html',NULL,NULL,NULL,NULL,'Pending','2026-10-15 07:42:49','2026-10-15 07:42:49');
INSERT INTO "companies" VALUES(131,'ChainGPT','https://www.chaingpt.org','chaingpt.org','ai','','remote','africa_region','https://apply.workable.com/chaingpt/j/454A921D4B/','https://jobs.workable.com/company/nvh46VrdnJAJUewq6F6hE9/jobs-at-chaingpt',NULL,NULL,NULL,NULL,'Pending','2026-10-15 07:42:54','2026-10-15 07:42:54');
INSERT INTO "companies" VALUES(132,'Bitovi','https://www.bitovi.com','bitovi.com','consultancy','','remote','explicit_ghana','https://bitovi.applytojob.com/apply/Ktw7pHEC3d/Offshore-Fullstack-Engineer-AI-Enabled','https://bitovi.applytojob.com/apply','Bitovi is a digital consultancy that partners with leading brands to design, build, and optimize complex web and software systems. They emphasize hands-on project management, scalable engineering, and DevOps across platforms.

What they do (core services)
- End-to-end product development and modernization for web apps and digital platforms
- Microservices architecture, cloud-native deployments, and DevOps/CI-CD
- UX, UI, and design systems (including scalable Figma design systems)
- Discovery and product strategy, with guided redesigns and long-term ownership models
- Migration and platform modernization (e.g., transitioning workflows to modern runtimes like Temporal Cloud)

Products/services they build
- Scalable e-commerce and ordering infrastructure (unified platforms across multiple brands)
- Microservice-based backends and hybrid/Cloud-native deployments
- High-availability workflow platforms (e.g., Temporal-based migrations)
- Maintained design systems and frontend architectures for premium brands

Customers highlighted
- Yum brands (KFC, Taco Bell, Pizza Hut, Habit Burger Grill) for a unified ordering platform
- Coinbase, for migrating 300+ namespaces/services to Temporal Cloud without downtime
- Christie’s, for a prestige-focused website redesign and scalable design system

Tech stack (implied from case highlights)
- Microservices architecture and DevOps tooling
- Temporal Cloud (and temporal-based workflows)
- Private networking and encrypted payloads (security-focused deployments)
- Web/mobile/web-aggregator integrations for unified ordering
- Design systems and modern frontend design (Figma-based system)
- Scalable infrastructure to support multiple brands and high-traffic sites

In short, Bitovi is a high-end digital transformation partner that builds scalable web and backend platforms, migrates complex workflow systems to modern runtimes, and delivers design-driven, maintainable experiences for large consumer brands and fintechs.',NULL,'{"lead": "Client work rewards engineers who can drop into an unfamiliar setup and work out what the client actually needs. The harder part is leaving something that still runs after handover. Some of that work:", "bullets": [{"fact_id": "client-facing-delivery", "title": "Client-Facing Delivery", "text": "At Turing I exceeded client KPIs for data accuracy and volume, helping take the team to #1 in dataset quality on client-verified benchmarks; at BoaSoft I shipped a RAG platform built around the client''s own documents."}, {"fact_id": "infrastructure-as-code", "title": "Infrastructure as Code", "text": "I design scalable AWS environments with Terraform and Docker, including a secure multi-tier VPC and modular application layers, so environments are reproducible across clients."}, {"fact_id": "gitops-secrets", "title": "GitOps & Secrets", "text": "I implement GitOps delivery with Argo CD, treating Git as the single source of truth for cluster state, and inject runtime credentials from HashiCorp Vault to keep secrets out of images and repositories."}], "provider": "none", "model": "deterministic", "grounded": true, "fallback_reason": null, "generated_at": "2026-10-15 07:47:31"}',NULL,'Sent','2026-10-15 07:42:59','2026-10-15 07:50:48');
INSERT INTO "companies" VALUES(133,'OpenFn','http://www.openfn.org','openfn.org','general_startup','','remote','africa_region','https://jobs.workable.com/view/jRkT98KafNLJ4cuBUkiaF7/remote-principal-software-engineer-in-south-africa-at-openfn','https://www.openfn.org/careers','OpenFn provides an open-source, developer-friendly workflow automation platform designed for public sector and NGO use. Key points:

- What they do: Connects web apps, AI tools, registries, databases, and legacy systems to automate delivery of public services. Aims to help governments and NGOs modernize and scale digital public services with AI-enabled orchestration and end-to-end automation.
- Products/services: 
  - OpenFn Workflow Automation Platform (visual Workflow Builder) for building cross-system automations.
  - 100+ pre-built Adaptors to connect to apps, web APIs, databases, file exports (open source).
  - OpenFn-hosted SaaS option and full on-premise deployment (100% open source; portable across deployments).
  - Dev tools: CLI, Smart IDE, open source docs/community for rapid development.
  - Monitoring and reliability: centralized history, audit trails, failure retries, 24/7 monitoring, fault-tolerant, auto-healing, auto-scaling.
  - Deployment and support options: expert deployment help, managed services, enterprise support, partner network.
  - Data and security emphasis: trusted by governments and NGOs; emphasizes secure, reliable, scalable, standards-based solutions; protection of beneficiary data.
- Customers: Governments and NGOs worldwide (40+ countries), including public service deployments and Digital Public Goods ecosystems. They work with government digital transformation teams and NGOs.
- Tech stack / architecture: 
  - Open source software core (platform + docs) with 70+ open source Adaptors for various integrations.
  - Visual workflow builder for designing automations; code-friendly for complex logic.
  - Version control, locking, idempotent API services.
  - Infrastructure features: queue-based processing, fault-tolerant architecture, auto-healing, auto-scaling.
  - Deployment flexibility: hosted SaaS or on-premise/server deployments; cross-cloud/ on-prem portability.
  - Monitoring and auditing: comprehensive history, audit trails, failure retry mechanisms.
  
In short: OpenFn is an open-source, developer-centric workflow automation platform that links diverse apps and data sources to automate public services for governments and NGOs, offering a visual builder, 70+ adapters, deployment flexibility (SaaS or on-prem), strong reliability/security features, and enterprise support.',NULL,'{"lead": "Startups need to ship fast without the platform falling over. Automating the slow, error-prone parts is how I make both possible:", "bullets": [{"fact_id": "infrastructure-velocity", "title": "Infrastructure Velocity", "text": "I provision production-ready AWS infrastructure with Terraform and Docker, including a secure multi-tier VPC and modular application layers."}, {"fact_id": "fast-feedback-loops", "title": "Fast Feedback Loops", "text": "I built a cost-optimized Jenkins CI/CD engine with EC2 Spot agents that auto-scale with build queue depth, speeding up developer feedback while cutting compute cost."}, {"fact_id": "developer-self-service", "title": "Developer Self-Service", "text": "I deployed Prometheus, Loki, Grafana, and Jaeger with self-service dashboards that give developers on-demand insight into their environments and error logs."}], "provider": "none", "model": "deterministic", "grounded": true, "fallback_reason": null, "generated_at": "2026-10-15 07:47:36"}',NULL,'Sent','2026-10-15 07:43:08','2026-10-15 07:51:32');
INSERT INTO "companies" VALUES(134,'Anablock','https://anablock.com','anablock.com','ai','','remote','explicit_ghana','https://bebee.com/gh/jobs/ai-ml-software-engineer-remote-ghana-anablock--theirstack-666797714','https://nextleap.app/company/anablock/jobs',NULL,NULL,NULL,NULL,'Pending','2026-10-15 07:43:13','2026-10-15 07:43:13');
INSERT INTO "companies" VALUES(135,'BLVCK SAPPHIRE','https://www.blvcksapphire.com','blvcksapphire.com','ai','','remote','explicit_ghana','https://relomote.com/jobs/frontend-engineer-mobile-web-190759558','https://www.blvcksapphire.com/careers',NULL,NULL,NULL,NULL,'Pending','2026-10-15 07:43:18','2026-10-15 07:43:18');
INSERT INTO "companies" VALUES(136,'Mirantly','https://www.mirantly.com','mirantly.com','ai','','remote','explicit_ghana','https://techjobsinghana.com/tjig-jobs/founding-senior-software-engineer/','https://www.mirantly.com/careers',NULL,NULL,NULL,NULL,'Pending','2026-10-15 07:43:22','2026-10-15 07:44:27');
INSERT INTO "companies" VALUES(137,'Adaptive Computer Solutions (ACS Ghana)','https://www.acsghana.com','acsghana.com','consultancy','North Legon, Accra, Ghana','local','ghana_based',NULL,NULL,'Enterprise software development house and digital transformation partner in Ghana building scalable cloud platforms, microservices, and telecom/fintech integrations for clients like MTN and Stanbic Bank.',NULL,'{"lead": "Client work rewards engineers who can drop into an unfamiliar setup and work out what the client actually needs. The harder part is leaving something that still runs after handover. Some of that work:", "bullets": [{"fact_id": "client-facing-delivery", "title": "Client-Facing Delivery", "text": "At Turing I exceeded client KPIs for data accuracy and volume, helping take the team to #1 in dataset quality on client-verified benchmarks; at BoaSoft I shipped a RAG platform built around the client''s own documents."}, {"fact_id": "infrastructure-as-code", "title": "Infrastructure as Code", "text": "I design scalable AWS environments with Terraform and Docker, including a secure multi-tier VPC and modular application layers, so environments are reproducible across clients."}, {"fact_id": "gitops-secrets", "title": "GitOps & Secrets", "text": "I implement GitOps delivery with Argo CD, treating Git as the single source of truth for cluster state, and inject runtime credentials from HashiCorp Vault to keep secrets out of images and repositories."}], "provider": "none", "model": "deterministic", "grounded": true, "fallback_reason": null, "generated_at": "2026-10-15 22:16:00"}',NULL,'Sent','2026-10-15 22:15:07','2026-10-15 22:17:38');
CREATE TABLE contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
        full_name TEXT,
        title TEXT,
        email TEXT NOT NULL UNIQUE COLLATE NOCASE,
        source TEXT CHECK(source IS NULL OR source IN ('hunter', 'prospeo', 'apify', 'manual')),
        confidence_score INTEGER,
        verification_status TEXT CHECK(verification_status IS NULL OR verification_status IN ('valid', 'invalid', 'accept_all', 'unknown')),
        email_kind TEXT CHECK(email_kind IS NULL OR email_kind IN ('person', 'departmental', 'generic')),
        is_primary INTEGER NOT NULL DEFAULT 0 CHECK(is_primary IN (0, 1)),
        created_at TEXT,
        updated_at TEXT
    );
INSERT INTO "contacts" VALUES(1,1,NULL,NULL,'contact@pepapay.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:23:10');
INSERT INTO "contacts" VALUES(2,2,NULL,NULL,'hello@solvanesystems.com','apify',NULL,'invalid','generic',0,'2026-10-10 12:24:58','2026-10-10 12:27:57');
INSERT INTO "contacts" VALUES(3,3,NULL,NULL,'info@dodystack.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:26');
INSERT INTO "contacts" VALUES(4,6,NULL,NULL,'hr@devarps.com','apify',NULL,'unknown','departmental',0,'2026-10-10 12:24:58','2026-10-11 05:39:28');
INSERT INTO "contacts" VALUES(5,7,NULL,NULL,'info@exquode.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(6,8,NULL,NULL,'info@gammatechgh.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(7,9,NULL,NULL,'info@triaxistechnologies.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(8,10,NULL,NULL,'hello@apex-meta.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(9,11,NULL,NULL,'office@infotypeghana.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(10,12,NULL,NULL,'info@zilotechnologies.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(11,14,NULL,NULL,'info@wantechsolutions.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(12,15,NULL,NULL,'careers@esolutionsghana.com','apify',NULL,'invalid','departmental',0,'2026-10-10 12:24:58','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(13,16,NULL,NULL,'info@digitsndata.com','apify',NULL,NULL,'generic',0,'2026-10-10 12:24:58','2026-10-10 12:24:58');
INSERT INTO "contacts" VALUES(14,18,NULL,NULL,'hello@demannytechconsult.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(15,19,NULL,NULL,'info@mawulikode.com','apify',NULL,NULL,'generic',0,'2026-10-10 12:24:58','2026-10-10 12:24:58');
INSERT INTO "contacts" VALUES(16,25,NULL,NULL,'hello@acloe.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(17,26,NULL,NULL,'teamprogrammers1@gmail.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(18,27,NULL,NULL,'info@samasoftech.net','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(19,28,NULL,NULL,'emmaktech@gmail.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(20,34,NULL,NULL,'info@telenet.com.gh','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(21,35,NULL,NULL,'info@telesol.com.gh','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(22,36,NULL,NULL,'info@boldnetgh.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(23,38,NULL,NULL,'hello@coratechai.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(24,41,NULL,NULL,'info@kaizentech.tech','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(25,43,NULL,NULL,'michael.ofeor@niiosalabs.com','apify',NULL,NULL,'person',1,'2026-10-10 12:24:58','2026-10-10 12:24:58');
INSERT INTO "contacts" VALUES(26,45,NULL,NULL,'careers@selescribe.com','apify',NULL,'invalid','departmental',1,'2026-10-10 12:24:58','2026-10-11 05:39:28');
INSERT INTO "contacts" VALUES(27,46,NULL,NULL,'engineering@photonai.ai','apify',NULL,'unknown','departmental',1,'2026-10-10 12:24:58','2026-10-11 05:39:28');
INSERT INTO "contacts" VALUES(28,48,NULL,NULL,'info@m-kopa.com','apify',NULL,NULL,'generic',0,'2026-10-10 12:24:58','2026-10-10 12:24:58');
INSERT INTO "contacts" VALUES(29,49,NULL,NULL,'hello@risklabs.co','apify',NULL,NULL,'generic',0,'2026-10-10 12:24:58','2026-10-10 12:24:58');
INSERT INTO "contacts" VALUES(30,50,NULL,NULL,'hello@celsusos.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(31,51,NULL,NULL,'team@railway.com','apify',NULL,NULL,'generic',0,'2026-10-10 12:24:58','2026-10-10 12:24:58');
INSERT INTO "contacts" VALUES(32,55,NULL,NULL,'careers@hostnownow.com','apify',NULL,'invalid','departmental',0,'2026-10-10 12:24:58','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(33,63,NULL,NULL,'hello@orgmento.com','apify',NULL,NULL,'generic',0,'2026-10-10 12:24:58','2026-10-10 12:24:58');
INSERT INTO "contacts" VALUES(34,64,NULL,NULL,'info@teksol.com','apify',NULL,'invalid','generic',0,'2026-10-10 12:24:58','2026-10-15 06:57:50');
INSERT INTO "contacts" VALUES(35,65,NULL,NULL,'ammeterlabs@gmail.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(36,66,NULL,NULL,'info@excedi.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(37,68,NULL,NULL,'info@medirevs.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(38,72,NULL,NULL,'info@qknowedtech.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(39,74,NULL,NULL,'info@edfrica.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(40,77,NULL,NULL,'info@syllabusgh.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(41,79,NULL,NULL,'hello@tudu.africa','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(42,81,NULL,NULL,'info@shopbeta.com.gh','apify',NULL,'invalid','generic',0,'2026-10-10 12:24:58','2026-10-10 12:28:04');
INSERT INTO "contacts" VALUES(43,82,NULL,NULL,'hello@tezeon.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(44,84,NULL,NULL,'info@ghvendors.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(45,86,NULL,NULL,'recruitment@virtualinfosecafrica.com','apify',NULL,NULL,'departmental',0,'2026-10-10 12:24:58','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(46,87,NULL,NULL,'info@cyber-hawk.com','apify',NULL,NULL,'generic',0,'2026-10-10 12:24:58','2026-10-10 12:24:58');
INSERT INTO "contacts" VALUES(47,88,NULL,NULL,'info@kasazon.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(48,89,NULL,NULL,'info@bochsystems.net','apify',NULL,NULL,'generic',0,'2026-10-10 12:24:58','2026-10-10 12:24:58');
INSERT INTO "contacts" VALUES(49,90,NULL,NULL,'info@oosecgh.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(50,91,NULL,NULL,'info@slammghana.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(51,92,NULL,NULL,'info@kronixshield.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(52,95,NULL,NULL,'info@lunartribe.tech','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(53,96,NULL,NULL,'info@bigdataghana.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(54,97,NULL,NULL,'info@beronintelligence.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(55,99,NULL,NULL,'info@mogitalanalytics.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(56,100,NULL,NULL,'info@datamonkapp.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(57,101,NULL,NULL,'data@acnghana.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(58,102,NULL,NULL,'info@myfigtech.com','apify',NULL,NULL,'generic',0,'2026-10-10 12:24:58','2026-10-10 12:24:58');
INSERT INTO "contacts" VALUES(59,103,NULL,NULL,'hello@daabo.io','apify',NULL,NULL,'generic',0,'2026-10-10 12:24:58','2026-10-10 12:24:58');
INSERT INTO "contacts" VALUES(60,104,NULL,NULL,'info@ridewithmaya.com','apify',NULL,NULL,'generic',0,'2026-10-10 12:24:58','2026-10-10 12:24:58');
INSERT INTO "contacts" VALUES(61,105,NULL,NULL,'info@wonfliki.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(62,106,NULL,NULL,'info@completefarmer.com','apify',NULL,NULL,'generic',0,'2026-10-10 12:24:58','2026-10-10 12:24:58');
INSERT INTO "contacts" VALUES(63,108,NULL,NULL,'careers@agrisat.gh','apify',NULL,'unknown','departmental',1,'2026-10-10 12:24:58','2026-10-11 05:39:28');
INSERT INTO "contacts" VALUES(64,109,NULL,NULL,'hello@sesitechnologies.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(65,112,NULL,NULL,'info@xcelerateak.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(66,113,NULL,NULL,'info@modularpath.dev','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(67,115,NULL,NULL,'hello@clevertech.studio','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:29');
INSERT INTO "contacts" VALUES(68,116,NULL,NULL,'team@akanexus.com','apify',NULL,'unknown','generic',0,'2026-10-10 12:24:58','2026-10-11 05:32:29');
INSERT INTO "contacts" VALUES(69,117,NULL,NULL,'info@abeyiestudios.com','apify',NULL,NULL,'generic',0,'2026-10-10 12:24:58','2026-10-10 12:24:58');
INSERT INTO "contacts" VALUES(70,119,NULL,NULL,'info@4th-ir.com','apify',NULL,NULL,'generic',0,'2026-10-10 12:24:58','2026-10-10 12:24:58');
INSERT INTO "contacts" VALUES(71,106,'Desmond Koney','CEO','desmond@completefarmer.com','hunter',94,'valid','person',0,'2026-10-11 05:23:11','2026-10-11 05:23:11');
INSERT INTO "contacts" VALUES(72,106,'Hajaratu Issahaka','Director of Operations','hajaratu.issahaka@completefarmer.com','hunter',74,'valid','person',0,'2026-10-11 05:23:11','2026-10-11 05:23:11');
INSERT INTO "contacts" VALUES(73,106,'Gilbert Tackie','Innovation Manager','gilbert.tackie@completefarmer.com','hunter',73,'valid','person',0,'2026-10-11 05:23:11','2026-10-11 05:23:11');
INSERT INTO "contacts" VALUES(74,106,'John Ackumey','Regional Operations Manager','john.ackumey@completefarmer.com','hunter',72,'valid','person',0,'2026-10-11 05:23:11','2026-10-11 05:23:11');
INSERT INTO "contacts" VALUES(75,106,'Daniel Buernor','Warehouse Manager','daniel.buernor@completefarmer.com','hunter',70,'valid','person',0,'2026-10-11 05:23:11','2026-10-11 05:23:11');
INSERT INTO "contacts" VALUES(76,106,'Umar Alhassan','Operations Manager','umar.alhassan@completefarmer.com','hunter',69,'valid','person',0,'2026-10-11 05:23:11','2026-10-11 05:23:11');
INSERT INTO "contacts" VALUES(77,106,'Salifu Rafik','Sustainable Agriculture Agronomist','rafik.salifu@completefarmer.com','hunter',98,'unknown','person',0,'2026-10-11 05:23:11','2026-10-11 05:23:11');
INSERT INTO "contacts" VALUES(78,106,'Shuaib Derby','Product Associate','shuaib.derby@completefarmer.com','hunter',95,'unknown','person',0,'2026-10-11 05:23:11','2026-10-11 05:23:11');
INSERT INTO "contacts" VALUES(79,106,'Samuel Aggrey','Talent Acquisition Lead','samuel.aggrey@completefarmer.com','hunter',95,'valid','person',1,'2026-10-11 05:23:11','2026-10-11 05:40:45');
INSERT INTO "contacts" VALUES(80,106,'Baaba Toffah','ESG Manager','baaba.toffah@completefarmer.com','hunter',95,'unknown','person',0,'2026-10-11 05:23:11','2026-10-11 05:23:11');
INSERT INTO "contacts" VALUES(83,15,'Yaovi Amavi','Support Manager','yaovi@esolutionsghana.com','hunter',78,'valid','person',0,'2026-10-11 05:32:27','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(84,15,'Luqman Ainoo','Technical Consultant','luqman@esolutionsghana.com','hunter',99,'unknown','person',0,'2026-10-11 05:32:27','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(85,15,'Alfred Tackie-Quaye','Multimedia Consultant','alfred@esolutionsghana.com','hunter',98,'unknown','person',0,'2026-10-11 05:32:27','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(86,15,'Eric Owusu','Technical Consultant','eric@esolutionsghana.com','hunter',98,'unknown','person',0,'2026-10-11 05:32:27','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(87,15,'Alex Acquah','IT Consultant','alex@esolutionsghana.com','hunter',98,'valid','person',0,'2026-10-11 05:32:27','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(88,15,'Annabella Ishak','Technical Project Coordinator','annabella@esolutionsghana.com','hunter',97,'unknown','person',0,'2026-10-11 05:32:27','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(89,15,'Loretta Larbi','Administrative Assistant','loretta@esolutionsghana.com','hunter',97,'unknown','person',0,'2026-10-11 05:32:27','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(90,15,'Telvin Varfley','Technical Consultant','telvin@esolutionsghana.com','hunter',96,'unknown','person',0,'2026-10-11 05:32:27','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(91,15,'Isaac Owusu','Technical Consultant','isaac@esolutionsghana.com','hunter',96,'unknown','person',0,'2026-10-11 05:32:27','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(92,15,NULL,'Other Person','victor@esolutionsghana.com','hunter',95,'unknown','person',0,'2026-10-11 05:32:27','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(93,15,'Olayiwola Allen','Chief Technology Officer','olayiwola@esolutionsghana.com','hunter',99,'valid','person',1,'2026-10-11 05:32:27','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(94,16,'Deji Oguntonade','Managing Director','doguntonade@digitsndata.com','hunter',95,'valid','person',0,'2026-10-11 05:32:27','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(95,16,'Lawrence Agbemava','Lead Software Engineer','lagbemava@digitsndata.com','hunter',44,'valid','person',1,'2026-10-11 05:32:27','2026-10-11 05:40:48');
INSERT INTO "contacts" VALUES(96,16,NULL,'Other Person','vafudego@digitsndata.com','hunter',10,'unknown','person',0,'2026-10-11 05:32:27','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(97,16,'Sophie Nanteza','Other Person','snanteza@digitsndata.com','hunter',15,'unknown','person',0,'2026-10-11 05:32:27','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(98,19,'Mawuli Denteh','Founder & CEO','mawuli.denteh@mawulikode.com','hunter',99,'valid','person',1,'2026-10-11 05:32:27','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(99,25,NULL,'Other Person','toad@acloe.com','hunter',83,'accept_all','person',1,'2026-10-11 05:32:27','2026-10-11 05:40:50');
INSERT INTO "contacts" VALUES(100,25,NULL,'Other Person','dhanffz@acloe.com','hunter',74,'unknown','person',0,'2026-10-11 05:32:27','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(105,46,NULL,'Other Person','archangel@photonai.ai','hunter',80,'unknown','person',0,'2026-10-11 05:32:27','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(106,46,NULL,'Other Person','nio@photonai.ai','hunter',74,'unknown','person',0,'2026-10-11 05:32:27','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(107,55,'Lydia Aka','Customer Service Agent','lydia@hostnownow.com','hunter',79,'unknown','person',0,'2026-10-11 05:32:27','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(108,55,'Ayodeji Niyi-Adesola','Chief Executive Officer (CEO), HostNowNow','ayodeji@hostnownow.com','hunter',82,'valid','person',1,'2026-10-11 05:32:27','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(109,63,'Hamza Umar','Software Engineer','hamza.umar@orgmento.com','hunter',79,'unknown','person',0,'2026-10-11 05:32:27','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(110,63,'Rakan Mahamudu','Finance Project Lead','rakan.mahamudu@orgmento.com','hunter',70,'unknown','person',0,'2026-10-11 05:32:27','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(111,63,'Shanoon Issaka','Software Engineer','shanoon.issaka@orgmento.com','hunter',70,'unknown','person',0,'2026-10-11 05:32:27','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(112,63,'Larkuo Wilson-Tetteh','Software Engineer','larkuo.wilson-tetteh@orgmento.com','hunter',70,'valid','person',0,'2026-10-11 05:32:27','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(113,63,'Patrick Simpe-Asante','Co-founder and Director of Software Engineering','patrick.simpe-asante@orgmento.com','hunter',80,'accept_all','person',1,'2026-10-11 05:32:27','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(114,63,'Phyllis Boakye Simpe-Asante','Co-Founder and Director','phyllis.boakyesimpeasante@orgmento.com','hunter',81,'accept_all','person',0,'2026-10-11 05:32:27','2026-10-11 05:32:27');
INSERT INTO "contacts" VALUES(117,86,'Eddie Sekyere','Brand and Communications Executive','esekyere@virtualinfosecafrica.com','hunter',99,'unknown','person',0,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(118,86,'Fafa Asamoah','IT Systems Engineer','fasamoah@virtualinfosecafrica.com','hunter',99,'unknown','person',0,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(119,86,'Nicholas Owusu','Security Analyst','nowusu@virtualinfosecafrica.com','hunter',98,'unknown','person',0,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(120,86,'Collins Marfo','Other Person','cmarfo@virtualinfosecafrica.com','hunter',97,'unknown','person',0,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(121,86,'Bennett Owusu-Ansah','Systems Engineer','bowusu-ansah@virtualinfosecafrica.com','hunter',96,'unknown','person',0,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(122,86,'Lawrence Narh','Other Person','lnarh@virtualinfosecafrica.com','hunter',95,'valid','person',0,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(123,86,'Jesse Okai','Network Security Engineer','jokai@virtualinfosecafrica.com','hunter',92,'unknown','person',0,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(124,86,'Michael Osanquaye','Senior Security Analyst','mosanquaye@virtualinfosecafrica.com','hunter',84,'unknown','person',0,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(125,86,'Kingsford Mensah','Cybersecurity Analyst','kmensah@virtualinfosecafrica.com','hunter',83,'unknown','person',0,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(126,86,'Newton Oyatey','Network Security Engineer','noyatey@virtualinfosecafrica.com','hunter',83,'unknown','person',0,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(127,86,'Daniel Lamptey','Technical Director','dlamptey@virtualinfosecafrica.com','hunter',98,'valid','person',1,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(128,87,'Callum Kottis','Senior Vice President, Technical Delivery','callum@cyber-hawk.com','hunter',74,'invalid','person',1,'2026-10-11 05:32:28','2026-10-11 07:00:55');
INSERT INTO "contacts" VALUES(129,87,'Chris Fleming','Chief Executive Officer','chris@cyber-hawk.com','hunter',78,'accept_all','person',0,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(130,89,'Olusola Damilare','Chief Technology Officer','olusola@bochsystems.net','hunter',79,'accept_all','person',1,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(131,89,NULL,'Other Person','princewill.chioma@bochsystems.net','hunter',75,'unknown','person',0,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(132,89,NULL,'Other Person','tochukwu.uzomba@bochsystems.net','hunter',10,'unknown','person',0,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(133,90,'Gervin Appiah','Chief Security Officer','gervinappiah@oosecgh.com','hunter',84,'accept_all','person',1,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(134,90,NULL,'Other Person','saraok@oosecgh.com','hunter',80,'unknown','person',0,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(135,90,'Ryan Michael','Other Person','ryanmichael@oosecgh.com','hunter',85,'unknown','person',0,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(136,91,'Jonathan Asamoah','IT Support Intern','jasamoah@slammghana.com','hunter',99,'unknown','person',0,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(137,91,'Stella Asiedua','Other Person','sasiedua@slammghana.com','hunter',98,'valid','person',1,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(138,95,'Nutifafa Amedior','Business Intelligence Lead','nutifafa.amedior@lunartribe.tech','hunter',95,'valid','person',1,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(139,96,'Henry Baffoe','Managing Director & Co-Founder','henry.baffoe@bigdataghana.com','hunter',96,'valid','person',1,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(140,96,'Yaa Fordwour','Finance and Administration Manager','yaa.fordwour@bigdataghana.com','hunter',95,'valid','person',0,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(141,96,'Emmanuel Kyei-Baffour','Cloud Support Engineer','emmanuel.kyei-baffour@bigdataghana.com','hunter',99,'unknown','person',0,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(142,96,'Isaac Kwarteng','AI Engineer','isaac@bigdataghana.com','hunter',99,'valid','person',0,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(143,96,'Gertrude Chichi','Cloud Support Engineer','gertrude.chichi@bigdataghana.com','hunter',98,'valid','person',0,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(144,96,'Akwasi Anto','Data and AI Engineer','akwasi.anto@bigdataghana.com','hunter',97,'valid','person',0,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(145,102,'Nayram Mensah','Chief Technology Officer','nayram@myfigtech.com','hunter',95,'valid','person',1,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(146,103,'David Igiebor','Co-Founder and CTO','david@getdaabo.com','hunter',98,'valid','person',1,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(147,104,'Alfred Kissiedu Ludwig','Co-Founder','alfred@ridewithmaya.com','hunter',74,'accept_all','person',1,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(148,109,'Cynthia Antwi','Head Of Operations & HR','cynthia@sesitechnologies.com','hunter',79,'unknown','person',0,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(149,109,'Emmanuel Kyei','Director of Business Development','emmanuel@sesitechnologies.com','hunter',79,'valid','person',0,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(150,109,'Martin Avorgah','Hardware Development Engineer','martin@sesitechnologies.com','hunter',78,'valid','person',0,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(151,109,'Pauline Atikpo','Executive Assistant','pauline@sesitechnologies.com','hunter',42,'unknown','person',0,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(152,109,'Isaac Sesi','Founder and CEO','isaac@sesitechnologies.com','hunter',85,'valid','person',1,'2026-10-11 05:32:28','2026-10-11 05:32:28');
INSERT INTO "contacts" VALUES(153,117,'Kwadwo Twum','Data Analyst','kwadwotwum@abeyiestudios.com','hunter',79,'unknown','person',0,'2026-10-11 05:32:29','2026-10-11 05:32:29');
INSERT INTO "contacts" VALUES(154,117,'Joycelyn Adjei','Sherock Participant','joycelynadjei@abeyiestudios.com','hunter',79,'unknown','person',0,'2026-10-11 05:32:29','2026-10-11 05:32:29');
INSERT INTO "contacts" VALUES(155,117,NULL,'Other Person','abeyieschmutz@abeyiestudios.com','hunter',75,'unknown','person',0,'2026-10-11 05:32:29','2026-10-11 05:32:29');
INSERT INTO "contacts" VALUES(156,117,'Nancy Kanyoke','Project Manager','nancy.kanyoke@abeyiestudios.com','hunter',74,'unknown','person',0,'2026-10-11 05:32:29','2026-10-11 05:32:29');
INSERT INTO "contacts" VALUES(157,117,'Clara Amewode','Executive Assistant','clara.amewode@abeyiestudios.com','hunter',73,'accept_all','person',0,'2026-10-11 05:32:29','2026-10-11 05:32:29');
INSERT INTO "contacts" VALUES(158,117,'Abeyie Bonsu Schmutz','Co-Founder','abeyie.bonsuschmutz@abeyiestudios.com','hunter',73,'accept_all','person',0,'2026-10-11 05:32:29','2026-10-11 05:32:29');
INSERT INTO "contacts" VALUES(159,117,'Joy Bonsu Schmutz','Co-Founder','joybonsuschmutz@abeyiestudios.com','hunter',81,'invalid','person',1,'2026-10-11 05:32:29','2026-10-11 07:00:56');
INSERT INTO "contacts" VALUES(160,119,'Nana Brown','Director of Innovation','n.brown@4th-ir.com','hunter',95,'valid','person',0,'2026-10-11 05:32:29','2026-10-11 05:32:29');
INSERT INTO "contacts" VALUES(161,119,'Khalida Ali','Software Engineer','k.ali@4th-ir.com','hunter',95,'unknown','person',0,'2026-10-11 05:32:29','2026-10-11 05:32:29');
INSERT INTO "contacts" VALUES(162,119,'Ato Toffah','Back End Developer','a.toffah@4th-ir.com','hunter',95,'unknown','person',0,'2026-10-11 05:32:29','2026-10-11 05:32:29');
INSERT INTO "contacts" VALUES(163,119,'Isaac Mensah','Sales and Marketing Specialist','i.mensah@4th-ir.com','hunter',95,'unknown','person',0,'2026-10-11 05:32:29','2026-10-11 05:32:29');
INSERT INTO "contacts" VALUES(164,119,'Mawunyo Avornyo','AI Engineer','m.avornyo@4th-ir.com','hunter',95,'valid','person',0,'2026-10-11 05:32:29','2026-10-11 05:32:29');
INSERT INTO "contacts" VALUES(165,119,'Angel Twumasi','DevOps Engineer','a.twumasi@4th-ir.com','hunter',95,'valid','person',0,'2026-10-11 05:32:29','2026-10-11 05:32:29');
INSERT INTO "contacts" VALUES(166,119,'Samuel Sackey','Frontend Developer','s.sackey@4th-ir.com','hunter',95,'unknown','person',0,'2026-10-11 05:32:29','2026-10-11 05:32:29');
INSERT INTO "contacts" VALUES(167,119,'Elizabeth Sekyi','Administrative Assistant','e.sekyi@4th-ir.com','hunter',95,'unknown','person',0,'2026-10-11 05:32:29','2026-10-11 05:32:29');
INSERT INTO "contacts" VALUES(168,119,'Derek Yendoh','AI/ML Engineer','d.yendoh@4th-ir.com','hunter',95,'unknown','person',0,'2026-10-11 05:32:29','2026-10-11 05:32:29');
INSERT INTO "contacts" VALUES(169,119,'Ephraim Adehenu','IT System Administrator','e.adehenu@4th-ir.com','hunter',95,'unknown','person',0,'2026-10-11 05:32:29','2026-10-11 05:32:29');
INSERT INTO "contacts" VALUES(170,119,'Zeeshan Khalid','Chief Technology Officer','z.khalid@4th-ir.com','hunter',97,'valid','person',1,'2026-10-11 05:32:29','2026-10-11 05:32:29');
INSERT INTO "contacts" VALUES(171,119,'Thomas Gustinis','Chief Executive Officer','t.gustinis@4th-ir.com','hunter',99,'valid','person',0,'2026-10-11 05:32:29','2026-10-11 05:32:29');
INSERT INTO "contacts" VALUES(172,6,'Richard Bunnah','Founder | CEO','richard@devarps.com','prospeo',NULL,'valid','person',1,'2026-10-11 05:39:28','2026-10-11 06:33:43');
INSERT INTO "contacts" VALUES(173,6,'Frank Abudey','Co-Founder / COO','frank@devarps.com','prospeo',NULL,'valid','person',0,'2026-10-11 05:39:28','2026-10-11 05:39:28');
INSERT INTO "contacts" VALUES(174,124,'Claudia Basogloyele','Finance Manager','claudia.basogloyele@turntabl.io','hunter',99,'unknown','person',0,'2026-10-15 07:03:44','2026-10-15 07:03:44');
INSERT INTO "contacts" VALUES(175,124,'Calvin Thomas','Director of Engineering','calvin.thomas@turntabl.io','hunter',96,'valid','person',1,'2026-10-15 07:03:44','2026-10-15 07:03:44');
INSERT INTO "contacts" VALUES(176,124,'Natalia Sharon','Head of Engineering','natalia.sharon@turntabl.io','hunter',95,'unknown','person',0,'2026-10-15 07:03:44','2026-10-15 07:03:44');
INSERT INTO "contacts" VALUES(177,124,'James Clelford','IT Operations Manager','james.clelford@turntabl.io','hunter',74,'valid','person',0,'2026-10-15 07:03:44','2026-10-15 07:03:44');
INSERT INTO "contacts" VALUES(178,124,'Papa Kofi Boahen','Software Engineer','papa.boahen@turntabl.io','hunter',99,'unknown','person',0,'2026-10-15 07:03:44','2026-10-15 07:03:44');
INSERT INTO "contacts" VALUES(179,124,'Rebekah Simmonds','Client Director','rebekah.simmonds@turntabl.io','hunter',99,'unknown','person',0,'2026-10-15 07:03:44','2026-10-15 07:03:44');
INSERT INTO "contacts" VALUES(180,124,'Abigail Appah','Software Engineer','abigail.appah@turntabl.io','hunter',99,'unknown','person',0,'2026-10-15 07:03:44','2026-10-15 07:03:44');
INSERT INTO "contacts" VALUES(181,124,'Comfort Yeboah','Client Engagement Manager','comfort.yeboah@turntabl.io','hunter',99,'unknown','person',0,'2026-10-15 07:03:44','2026-10-15 07:03:44');
INSERT INTO "contacts" VALUES(182,124,'Emmanuel Mortey','Software Engineer','emmanuel.mortey@turntabl.io','hunter',99,'unknown','person',0,'2026-10-15 07:03:44','2026-10-15 07:03:44');
INSERT INTO "contacts" VALUES(183,124,'Alfred Klu','Software Engineer','alfred.klu@turntabl.io','hunter',98,'unknown','person',0,'2026-10-15 07:03:45','2026-10-15 07:03:45');
INSERT INTO "contacts" VALUES(184,123,'Teddy Tagoe','Brand And Communications Manager','teddytagoe@expresspaygh.com','hunter',95,'unknown','person',0,'2026-10-15 07:04:02','2026-10-15 07:04:02');
INSERT INTO "contacts" VALUES(185,123,'Caleb Frimpong','Information Security Manager','calebfrimpong@expresspaygh.com','hunter',95,'unknown','person',0,'2026-10-15 07:04:02','2026-10-15 07:04:02');
INSERT INTO "contacts" VALUES(186,123,'Patrick Larbi','Customer Experience Manager','patricklarbi@expresspaygh.com','hunter',95,'valid','person',0,'2026-10-15 07:04:02','2026-10-15 07:04:02');
INSERT INTO "contacts" VALUES(187,123,'John Aggrey','Back End Developer','johnaggrey@expresspaygh.com','hunter',95,'valid','person',0,'2026-10-15 07:04:02','2026-10-15 07:04:02');
INSERT INTO "contacts" VALUES(188,123,'Daniel Frimpong','iOS Developer','danielfrimpong@expresspaygh.com','hunter',95,'valid','person',0,'2026-10-15 07:04:02','2026-10-15 07:04:02');
INSERT INTO "contacts" VALUES(189,123,'Godson Avettey','Other Person','godsonavettey@expresspaygh.com','hunter',95,'unknown','person',0,'2026-10-15 07:04:02','2026-10-15 07:04:02');
INSERT INTO "contacts" VALUES(190,123,'Alice Opoku','Other Person','aliceopoku@expresspaygh.com','hunter',95,'unknown','person',0,'2026-10-15 07:04:02','2026-10-15 07:04:02');
INSERT INTO "contacts" VALUES(191,123,'Claude Nai','Backend Engineer','claudenai@expresspaygh.com','hunter',95,'unknown','person',0,'2026-10-15 07:04:02','2026-10-15 07:04:02');
INSERT INTO "contacts" VALUES(192,123,'Confidence Honu','Operations Associate','confidencehonu@expresspaygh.com','hunter',95,'unknown','person',0,'2026-10-15 07:04:02','2026-10-15 07:04:02');
INSERT INTO "contacts" VALUES(193,123,'Kwabena Ampofo','Software Engineer','kwabenaampofo@expresspaygh.com','hunter',95,'unknown','person',0,'2026-10-15 07:04:02','2026-10-15 07:04:02');
INSERT INTO "contacts" VALUES(194,123,'Nii Tetteh','Chief Technology Officer (Current) / Partner at expressPay Ghana Limited','niitetteh@expresspaygh.com','hunter',99,'valid','person',1,'2026-10-15 07:04:02','2026-10-15 07:04:02');
INSERT INTO "contacts" VALUES(195,123,'Curtis Vanderpuije','Co-Founder and CEO','cvanderpuije@expresspaygh.com','hunter',95,'valid','person',0,'2026-10-15 07:04:02','2026-10-15 07:04:02');
INSERT INTO "contacts" VALUES(196,120,NULL,'Generic Inbox','info@bridgewaytec.com','apify',NULL,'unknown','generic',0,'2026-10-15 07:04:38','2026-10-15 07:04:38');
INSERT INTO "contacts" VALUES(197,120,NULL,NULL,'partner@bridgewaytec.com','apify',NULL,'unknown','person',1,'2026-10-15 07:04:38','2026-10-15 07:04:38');
INSERT INTO "contacts" VALUES(198,127,'Sean Escola','Chief Neuroscientist','sean.escola@protocol.ai','hunter',98,'valid','person',0,'2026-10-15 07:05:01','2026-10-15 07:05:01');
INSERT INTO "contacts" VALUES(199,127,'Rachel Garcia','People Operations Manager','rachel@protocol.ai','hunter',97,'valid','person',0,'2026-10-15 07:05:01','2026-10-15 07:05:01');
INSERT INTO "contacts" VALUES(200,127,'Anastasia Golovina','Pr And Communications Manager','anastasia@protocol.ai','hunter',96,'unknown','person',0,'2026-10-15 07:05:01','2026-10-15 07:05:01');
INSERT INTO "contacts" VALUES(201,127,'Alex Firmani','General Manager','alex@protocol.ai','hunter',95,'valid','person',0,'2026-10-15 07:05:01','2026-10-15 07:05:01');
INSERT INTO "contacts" VALUES(202,127,'Niki Gokani','Head of Customer Success','niki@protocol.ai','hunter',95,'valid','person',0,'2026-10-15 07:05:01','2026-10-15 07:05:01');
INSERT INTO "contacts" VALUES(203,127,'Victoria Devesty','Chief Operating Officer','victoria@protocol.ai','hunter',95,'valid','person',0,'2026-10-15 07:05:01','2026-10-15 07:05:01');
INSERT INTO "contacts" VALUES(204,127,'Danielle Andrzejewski','Chief Operating Officer','danielle.andrzejewski@protocol.ai','hunter',95,'valid','person',0,'2026-10-15 07:05:01','2026-10-15 07:05:01');
INSERT INTO "contacts" VALUES(205,127,'Stefanie Wykoff','Director of Human Resources','stefanie.wykoff@protocol.ai','hunter',95,'valid','person',0,'2026-10-15 07:05:01','2026-10-15 07:05:01');
INSERT INTO "contacts" VALUES(206,127,'Richard Chang','Marketing Lead','richard.chang@protocol.ai','hunter',99,'valid','person',0,'2026-10-15 07:05:01','2026-10-15 07:05:01');
INSERT INTO "contacts" VALUES(207,127,'Yiannis Psaras','Research Scientist','yiannis@protocol.ai','hunter',99,'unknown','person',0,'2026-10-15 07:05:01','2026-10-15 07:05:01');
INSERT INTO "contacts" VALUES(208,127,'Molly Mackinlay','Head of Engineering, Product, & Research Development','molly@protocol.ai','hunter',95,'valid','person',1,'2026-10-15 07:05:01','2026-10-15 07:05:01');
INSERT INTO "contacts" VALUES(209,126,'Shannon Lincoln','Chief Financial Officer','shannon.lincoln@oysterhr.com','hunter',99,'valid','person',0,'2026-10-15 07:05:20','2026-10-15 07:05:20');
INSERT INTO "contacts" VALUES(210,126,'Tony Jamous','Chairman','tony.jamous@oysterhr.com','hunter',97,'valid','person',0,'2026-10-15 07:05:20','2026-10-15 07:05:20');
INSERT INTO "contacts" VALUES(211,126,'Jennifer Fields','Director of Demand Generation','jennifer.fields@oysterhr.com','hunter',95,'valid','person',0,'2026-10-15 07:05:20','2026-10-15 07:05:20');
INSERT INTO "contacts" VALUES(212,126,'Alexandra McKay','Director of Product Marketing','alexandra.mckay@oysterhr.com','hunter',95,'valid','person',0,'2026-10-15 07:05:20','2026-10-15 07:05:20');
INSERT INTO "contacts" VALUES(213,126,'Jemma Thomas','Director of Legal and Compliance','jemma.thomas@oysterhr.com','hunter',95,'valid','person',0,'2026-10-15 07:05:20','2026-10-15 07:05:20');
INSERT INTO "contacts" VALUES(214,126,'Jelle Berends','VP of Revenue Operations','jelle.berends@oysterhr.com','hunter',95,'unknown','person',0,'2026-10-15 07:05:20','2026-10-15 07:05:20');
INSERT INTO "contacts" VALUES(215,126,'Patricia Piticas','Director of Employment Products','patricia.piticas@oysterhr.com','hunter',95,'unknown','person',0,'2026-10-15 07:05:20','2026-10-15 07:05:20');
INSERT INTO "contacts" VALUES(216,126,'Luis Franco','Senior Vice President of Operations','luis.franco@oysterhr.com','hunter',95,'valid','person',0,'2026-10-15 07:05:20','2026-10-15 07:05:20');
INSERT INTO "contacts" VALUES(217,126,'Karita Kasurinen','Director of Onboarding and Offboarding','karita.kasurinen@oysterhr.com','hunter',95,'valid','person',0,'2026-10-15 07:05:20','2026-10-15 07:05:20');
INSERT INTO "contacts" VALUES(218,126,'Sara Guerreiro','Director of Product Management','sara.guerreiro@oysterhr.com','hunter',95,'valid','person',0,'2026-10-15 07:05:20','2026-10-15 07:05:20');
INSERT INTO "contacts" VALUES(219,126,'Matt Machuga','VP Engineering','matt.machuga@oysterhr.com','hunter',99,'valid','person',1,'2026-10-15 07:05:20','2026-10-15 07:05:20');
INSERT INTO "contacts" VALUES(220,126,'Jakub Kratina','Director of Engineering','jakub.kratina@oysterhr.com','hunter',96,'valid','person',0,'2026-10-15 07:05:20','2026-10-15 07:05:20');
INSERT INTO "contacts" VALUES(221,122,'Keerthana Durairaj','HR Manager','keerthana@zethic.com','hunter',78,'valid','person',1,'2026-10-15 07:06:09','2026-10-15 07:06:09');
INSERT INTO "contacts" VALUES(222,122,'Varun Biju','Head of Delivery','varun@zethic.com','hunter',76,'valid','person',0,'2026-10-15 07:06:09','2026-10-15 07:06:09');
INSERT INTO "contacts" VALUES(223,122,'Swarnalata Shetty','Business Development Specialist','swarnalata@zethic.com','hunter',85,'unknown','person',0,'2026-10-15 07:06:09','2026-10-15 07:06:09');
INSERT INTO "contacts" VALUES(224,122,'Himanshu Kumar','Full Stack Developer','himanshu@zethic.com','hunter',79,'valid','person',0,'2026-10-15 07:06:09','2026-10-15 07:06:09');
INSERT INTO "contacts" VALUES(225,122,'Arpan Agrawal','Software Engineer','arpan@zethic.com','hunter',79,'unknown','person',0,'2026-10-15 07:06:09','2026-10-15 07:06:09');
INSERT INTO "contacts" VALUES(226,122,'Payal Sharma','Marketing Consultant','payal@zethic.com','hunter',79,'unknown','person',0,'2026-10-15 07:06:09','2026-10-15 07:06:09');
INSERT INTO "contacts" VALUES(227,122,'Manpreet Kaur','Executive Assistant','manpreet@zethic.com','hunter',78,'valid','person',0,'2026-10-15 07:06:09','2026-10-15 07:06:09');
INSERT INTO "contacts" VALUES(228,122,'Ananya Roy','Project Manager','ananya@zethic.com','hunter',78,'valid','person',0,'2026-10-15 07:06:09','2026-10-15 07:06:09');
INSERT INTO "contacts" VALUES(229,122,'Karthick T','HR and Finance Associate','karthick@zethic.com','hunter',77,'unknown','person',0,'2026-10-15 07:06:09','2026-10-15 07:06:09');
INSERT INTO "contacts" VALUES(230,122,'Magithar Sridhar','Product Manager','magithar@zethic.com','hunter',77,'valid','person',0,'2026-10-15 07:06:09','2026-10-15 07:06:09');
INSERT INTO "contacts" VALUES(231,125,NULL,'Generic Inbox','contact@direktdot.com','apify',NULL,'unknown','generic',0,'2026-10-15 07:06:36','2026-10-15 07:06:36');
INSERT INTO "contacts" VALUES(232,129,'Will Croft','Co-Founder and CTO','will@withboost.co','prospeo',NULL,'valid','person',1,'2026-10-15 07:42:06','2026-10-15 07:42:06');
INSERT INTO "contacts" VALUES(233,129,'Mary Roach','Co-Founder and COO','mary@boost.technology','prospeo',NULL,'valid','person',0,'2026-10-15 07:42:06','2026-10-15 07:42:06');
INSERT INTO "contacts" VALUES(234,132,'Paul Herzog','Director of Agile Project Management','pherzog@bitovi.com','hunter',85,'unknown','person',0,'2026-10-15 07:44:42','2026-10-15 07:44:42');
INSERT INTO "contacts" VALUES(235,132,'Levi Myers','Director of Product Design','levi@bitovi.com','hunter',84,'unknown','person',0,'2026-10-15 07:44:42','2026-10-15 07:44:42');
INSERT INTO "contacts" VALUES(236,132,'Kyle Gifford','Director of Consulting','kyle@bitovi.com','hunter',84,'valid','person',0,'2026-10-15 07:44:42','2026-10-15 07:44:42');
INSERT INTO "contacts" VALUES(237,132,'Chasen Hara','Learning and Development Manager','chasen@bitovi.com','hunter',84,'unknown','person',0,'2026-10-15 07:44:42','2026-10-15 07:44:42');
INSERT INTO "contacts" VALUES(238,132,'Mick Mcgrath','Director of Artificial Intelligence','mick@bitovi.com','hunter',83,'valid','person',0,'2026-10-15 07:44:42','2026-10-15 07:44:42');
INSERT INTO "contacts" VALUES(239,132,'Kevin Phillips','Director of Engineering','kevin@bitovi.com','hunter',82,'valid','person',1,'2026-10-15 07:44:42','2026-10-15 07:44:42');
INSERT INTO "contacts" VALUES(240,132,'Justin Meyer','Chief Executive Officer','justin@bitovi.com','hunter',81,'valid','person',0,'2026-10-15 07:44:42','2026-10-15 07:44:42');
INSERT INTO "contacts" VALUES(241,132,'Brian Tai','Sales Director','btai@bitovi.com','hunter',75,'unknown','person',0,'2026-10-15 07:44:42','2026-10-15 07:44:42');
INSERT INTO "contacts" VALUES(242,132,'Paula Strozak','Chief Operating Officer','paula@bitovi.com','hunter',75,'valid','person',0,'2026-10-15 07:44:42','2026-10-15 07:44:42');
INSERT INTO "contacts" VALUES(243,132,NULL,'Other Person','kosborn@bitovi.com','hunter',85,'unknown','person',0,'2026-10-15 07:44:42','2026-10-15 07:44:42');
INSERT INTO "contacts" VALUES(244,133,'Taylor Downs','Founder','taylor@openfn.org','hunter',85,'valid','person',0,'2026-10-15 07:44:48','2026-10-15 07:44:48');
INSERT INTO "contacts" VALUES(245,133,'Brandon Jackson','Head of Product','brandon@openfn.org','hunter',85,'unknown','person',0,'2026-10-15 07:44:48','2026-10-15 07:44:48');
INSERT INTO "contacts" VALUES(246,133,'Aleksa Krolls','Chief Operating Officer','aleksa@openfn.org','hunter',85,'valid','person',0,'2026-10-15 07:44:48','2026-10-15 07:44:48');
INSERT INTO "contacts" VALUES(247,133,'Bailly Rurangirwa','Growth Manager','bailly@openfn.org','hunter',79,'valid','person',0,'2026-10-15 07:44:48','2026-10-15 07:44:48');
INSERT INTO "contacts" VALUES(248,133,'Derek Treatman','Director of Innovation and Partnerships','derek@openfn.org','hunter',79,'valid','person',0,'2026-10-15 07:44:48','2026-10-15 07:44:48');
INSERT INTO "contacts" VALUES(249,133,'Stuart Corbishley','Chief Technology Officer','stuart@openfn.org','hunter',79,'valid','person',1,'2026-10-15 07:44:48','2026-10-15 07:44:48');
INSERT INTO "contacts" VALUES(250,133,'Catherine Sieberhagen','Head of Implementation','catherine@openfn.org','hunter',78,'valid','person',0,'2026-10-15 07:44:48','2026-10-15 07:44:48');
INSERT INTO "contacts" VALUES(251,133,'Jack Hilton','Head of Growth','jack@openfn.org','hunter',78,'valid','person',0,'2026-10-15 07:44:48','2026-10-15 07:44:48');
INSERT INTO "contacts" VALUES(252,133,'Precious Nwiko','Country Lead','precious@openfn.org','hunter',85,'unknown','person',0,'2026-10-15 07:44:48','2026-10-15 07:44:48');
INSERT INTO "contacts" VALUES(253,133,'Pius Kariuki','Solutions Engineer','pius@openfn.org','hunter',85,'valid','person',0,'2026-10-15 07:44:48','2026-10-15 07:44:48');
INSERT INTO "contacts" VALUES(254,131,'Mitchell G','Chief Human Resources Officer','mitchell@chaingpt.org','hunter',98,'valid','person',0,'2026-10-15 07:45:11','2026-10-15 07:45:11');
INSERT INTO "contacts" VALUES(255,131,'Vlad Nazar','Head of Business Development','vladnazar@chaingpt.org','hunter',97,'valid','person',0,'2026-10-15 07:45:11','2026-10-15 07:45:11');
INSERT INTO "contacts" VALUES(256,131,'Cameron French','Chief Compliance Officer','cameron@chaingpt.org','hunter',99,'valid','person',0,'2026-10-15 07:45:11','2026-10-15 07:45:11');
INSERT INTO "contacts" VALUES(257,131,'Uthman Sulyman','Community Manager','uthman@chaingpt.org','hunter',98,'valid','person',0,'2026-10-15 07:45:11','2026-10-15 07:45:11');
INSERT INTO "contacts" VALUES(258,131,NULL,'Other Person','gintare@chaingpt.org','hunter',96,'valid','person',0,'2026-10-15 07:45:11','2026-10-15 07:45:11');
INSERT INTO "contacts" VALUES(259,131,NULL,'Other Person','ariel@chaingpt.org','hunter',96,'valid','person',0,'2026-10-15 07:45:11','2026-10-15 07:45:11');
INSERT INTO "contacts" VALUES(260,131,NULL,'Other Person','rosemary@chaingpt.org','hunter',84,'unknown','person',0,'2026-10-15 07:45:11','2026-10-15 07:45:11');
INSERT INTO "contacts" VALUES(261,131,'Ilan Rakhmanov','Other Person','ilan@chaingpt.org','hunter',99,'valid','person',0,'2026-10-15 07:45:11','2026-10-15 07:45:11');
INSERT INTO "contacts" VALUES(262,131,'Muhammad Adnan Tariq','Chief Technology Officer','adnan@chaingpt.org','hunter',96,'valid','person',1,'2026-10-15 07:45:11','2026-10-15 07:45:11');
INSERT INTO "contacts" VALUES(263,130,'Archurst Agyarko','CEO','archurst@cosbyte.com','hunter',81,'unknown','person',1,'2026-10-15 07:45:16','2026-10-15 07:45:16');
INSERT INTO "contacts" VALUES(264,137,'Nana Kofi Aferi','Engineering Manager','kofi@acsint.io','prospeo',95,'valid','person',1,'2026-10-15 22:15:07','2026-10-15 22:15:07');
INSERT INTO "contacts" VALUES(265,137,'Kofi Amparbeng','Founder & Managing Director','kamparbeng@acsint.io','prospeo',95,'valid','person',0,'2026-10-15 22:15:07','2026-10-15 22:15:07');
CREATE TABLE inbox_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kind TEXT NOT NULL CHECK(kind IN ('reply', 'bounce', 'auto_reply', 'unsubscribe')),
        from_email TEXT,
        subject TEXT,
        imap_message_id TEXT NOT NULL UNIQUE,
        received_at TEXT,
        snippet TEXT,
        company_id INTEGER REFERENCES companies(id),
        contact_id INTEGER REFERENCES contacts(id),
        outreach_id INTEGER REFERENCES outreaches(id),
        created_at TEXT
    );
INSERT INTO "inbox_events" VALUES(1,'bounce','mailer-daemon@googlemail.com','Delivery Status Notification (Failure)','<6ac6c7de.0143c1f4.1f0a0d.0ba1.GMR@mx.google.com>','2026-10-07 15:29:50','** Address not found ** Your message wasn''t delivered to hello@solvanesystems.com because the address couldn''t be found, or is unable to receive mail. Learn more here: https://support.google.com/mail/?p=NoSuchUser The response was: 550 5.1.1 The emai',2,2,NULL,'2026-10-10 12:27:57');
INSERT INTO "inbox_events" VALUES(2,'bounce','mailer-daemon@googlemail.com','Delivery Status Notification (Failure)','<6ac6c8c1.829a157f.3112aa.0be2.GMR@mx.google.com>','2026-10-07 15:33:37','** Message blocked ** Your message to careers@esolutionsghana.com has been blocked. See technical details below for more information. Learn more here: https://aka.ms/EXOSmtpErrors (Warning: This link will take you to a third-party site) The response ',15,12,NULL,'2026-10-10 12:27:58');
INSERT INTO "inbox_events" VALUES(3,'bounce','mailer-daemon@googlemail.com','Delivery Status Notification (Failure)','<6ac6c9ab.32c57251.ec174.1cb5.GMR@mx.google.com>','2026-10-07 15:37:31','** Message not delivered ** Your message couldn''t be delivered to careers@selescribe.com because the remote server is misconfigured. See technical details below for more information. The response from the remote server was: 554 5.7.1 <careers@selescr',45,26,NULL,'2026-10-10 12:27:58');
INSERT INTO "inbox_events" VALUES(4,'bounce','mailer-daemon@googlemail.com','Delivery Status Notification (Failure)','<6ac6ca47.c32eea13.1e7d14.9900.GMR@mx.google.com>','2026-10-07 15:40:07','** Address not found ** Your message wasn''t delivered to careers@hostnownow.com because the address couldn''t be found, or is unable to receive mail. Learn more here: https://support.google.com/mail/?p=NoSuchUser The response was: The email account th',55,32,NULL,'2026-10-10 12:27:58');
INSERT INTO "inbox_events" VALUES(5,'bounce','mailer-daemon@googlemail.com','Delivery Status Notification (Failure)','<6ac78723.00d28814.274073.1f18.GMR@mx.google.com>','2026-10-08 05:05:55','** Address not found ** Your message wasn''t delivered to info@shopbeta.com.gh because the address couldn''t be found, or is unable to receive mail. The response from the remote server was: 550 5.1.1 User does not exist - <info@shopbeta.com.gh>',81,42,NULL,'2026-10-10 12:28:04');
INSERT INTO "inbox_events" VALUES(6,'auto_reply','mailer-daemon@googlemail.com','Delivery Status Notification (Delay)','<6ac8e08d.0bcc40a0.78c50.b373.GMR@mx.google.com>','2026-10-09 05:39:41','** Delivery incomplete ** There was a temporary problem delivering your message to info@teksol.com. Gmail will retry for 47 more hours. You''ll be notified if the delivery fails permanently. Learn more here: https://support.google.com/mail/answer/7720',64,34,NULL,'2026-10-10 12:28:15');
INSERT INTO "inbox_events" VALUES(7,'auto_reply','mailer-daemon@googlemail.com','Delivery Status Notification (Delay)','<6aca3dec.1dfadcc1.5ac7c.572c.GMR@mx.google.com>','2026-10-10 06:30:20','** Delivery incomplete ** There was a temporary problem delivering your message to info@teksol.com. Gmail will retry for 22 more hours. You''ll be notified if the delivery fails permanently. Learn more here: https://support.google.com/mail/answer/7720',64,34,NULL,'2026-10-11 07:00:48');
INSERT INTO "inbox_events" VALUES(8,'bounce','postmaster@stlghana.com','Undeliverable: Forward Deployed / Platform Engineer Application -
 Isaac Obo Enimil','<b6b9c78b-4d40-44c1-adcc-283aaebec6d2@STL-HQ-EX02.stlghana.com>','2026-10-11 06:40:12','Delivery has failed to these recipients or groups: callum@cyber-hawk.com<mailto:callum@cyber-hawk.com> The email address you entered couldn''t be found. Please check the recipient''s email address and try to resend the message. If the problem continues',87,128,NULL,'2026-10-11 07:00:55');
INSERT INTO "inbox_events" VALUES(9,'bounce','postmaster@abeyiestudios.com','Undeliverable: Forward Deployed / Platform Engineer Application -
 Isaac Obo Enimil','<ec605a27-0488-4a17-abb6-840ff4af8510@PA2P189MB2691.EURP189.PROD.OUTLOOK.COM>','2026-10-11 06:44:45','[https://products.office.com/en-us/CMSImages/Office365Logo_Orange.png?version=b8d100a9-0a8b-8e6a-88e1-ef488fee0470] Your message to joybonsuschmutz@abeyiestudios.com couldn''t be delivered. joybonsuschmutz wasn''t found at abeyiestudios.com. ioenimil O',117,159,NULL,'2026-10-11 07:00:56');
INSERT INTO "inbox_events" VALUES(10,'bounce','mailer-daemon@googlemail.com','Delivery Status Notification (Failure)','<6acbac9b.f44bb46d.41c17.4cb1.GMR@mx.google.com>','2026-10-11 08:34:51','** Message not delivered ** There was a problem delivering your message to info@teksol.com. See the technical details below. Learn more here: https://support.google.com/mail/answer/7720 The response was: The recipient server did not accept our reques',64,34,NULL,'2026-10-15 06:57:50');
INSERT INTO "inbox_events" VALUES(11,'reply','info@kaizentech.tech','Re:  Forward Deployed Engineer Application - Isaac Obo Enimil','<224546143444563968.0.v2@titan.email>','2026-10-14 12:25:03','Hi Enimil, Your email is well received, however there are no current open roles at Kaizen Technologies for the aforementioned related fields. Please do check back later, and keep an eye on our LinkedIn for future roles. All the best, Kaizen Technolog',41,24,10,'2026-10-15 06:58:50');
CREATE TABLE outreaches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER NOT NULL REFERENCES companies(id),
        contact_id INTEGER REFERENCES contacts(id),
        recipient_email TEXT NOT NULL,
        email_type TEXT NOT NULL CHECK(email_type IN ('initial', 'followup')),
        subject TEXT,
        message_id TEXT UNIQUE,
        in_reply_to TEXT,
        references_header TEXT,
        status TEXT NOT NULL CHECK(status IN ('SUCCESS', 'FAILED')),
        error TEXT,
        sent_at TEXT NOT NULL,
        cover_letter_path TEXT, body TEXT,
        UNIQUE(company_id, recipient_email, email_type, sent_at)
    );
INSERT INTO "outreaches" VALUES(1,1,1,'contact@pepapay.com','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<6ac6c7b7.5fb1dcdd.23b85.fe1a@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-07 22:29:12','Isaac_Obo_Enimil_Cover_Letter_PepaPay.pdf',NULL);
INSERT INTO "outreaches" VALUES(2,2,2,'hello@solvanesystems.com','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<6ac6c7da.41081df4.a4e3a.4d0b@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-07 22:29:49','Isaac_Obo_Enimil_Cover_Letter_Solvane_Systems.pdf',NULL);
INSERT INTO "outreaches" VALUES(3,3,3,'info@dodystack.com','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<6ac6c801.a6a2e554.1fbcb4.2a55@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-07 22:30:27','Isaac_Obo_Enimil_Cover_Letter_DODY_Stack.pdf',NULL);
INSERT INTO "outreaches" VALUES(4,6,4,'hr@devarps.com','initial','Forward Deployed / Platform Engineer Application - Isaac Obo Enimil','<6ac6c829.d3c9df1f.afab8.fe34@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-07 22:31:06','Isaac_Obo_Enimil_Cover_Letter_Devarps.pdf',NULL);
INSERT INTO "outreaches" VALUES(5,7,5,'info@exquode.com','initial','Forward Deployed / Platform Engineer Application - Isaac Obo Enimil','<6ac6c859.fadcb60d.16e2b1.2e94@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-07 22:31:57','Isaac_Obo_Enimil_Cover_Letter_Exquode.pdf',NULL);
INSERT INTO "outreaches" VALUES(6,10,8,'hello@apex-meta.com','initial','Forward Deployed / Platform Engineer Application - Isaac Obo Enimil','<6ac6c892.d3c9df1f.afab8.0fc8@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-07 22:32:51','Isaac_Obo_Enimil_Cover_Letter_Apex-Meta.pdf',NULL);
INSERT INTO "outreaches" VALUES(7,15,12,'careers@esolutionsghana.com','initial','Forward Deployed / Platform Engineer Application - Isaac Obo Enimil','<6ac6c8be.7b11d76c.2f4a6a.b9bb@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-07 22:33:37','Isaac_Obo_Enimil_Cover_Letter_eSolutions_Consulting.pdf',NULL);
INSERT INTO "outreaches" VALUES(8,25,16,'hello@acloe.com','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<6ac6c8e4.c9eda3e9.26a3ee.0dbe@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-07 22:34:13','Isaac_Obo_Enimil_Cover_Letter_Acloe_Technologies.pdf',NULL);
INSERT INTO "outreaches" VALUES(9,38,23,'hello@coratechai.com','initial','Forward Deployed Engineer Application - Isaac Obo Enimil','<6ac6c913.6e1d7bbd.32364.d1f9@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-07 22:35:02','Isaac_Obo_Enimil_Cover_Letter_Coratech_AI.pdf',NULL);
INSERT INTO "outreaches" VALUES(10,41,24,'info@kaizentech.tech','initial','Forward Deployed Engineer Application - Isaac Obo Enimil','<6ac6c947.b62143e1.8ac05.ab6b@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-07 22:35:53','Isaac_Obo_Enimil_Cover_Letter_Kaizen_Technologies.pdf',NULL);
INSERT INTO "outreaches" VALUES(11,43,25,'michael.ofeor@niiosalabs.com','initial','Forward Deployed Engineer Application - Isaac Obo Enimil','<6ac6c987.75747b7c.ea71c.40ac@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-07 22:36:56','Isaac_Obo_Enimil_Cover_Letter_NiiOsa_Labs.pdf',NULL);
INSERT INTO "outreaches" VALUES(12,45,26,'careers@selescribe.com','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<6ac6c9a9.88c14c61.3ae0c7.b773@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-07 22:37:30','Isaac_Obo_Enimil_Cover_Letter_SeleScribe.pdf',NULL);
INSERT INTO "outreaches" VALUES(13,46,27,'engineering@photonai.ai','initial','Forward Deployed Engineer Application - Isaac Obo Enimil','<6ac6c9db.c6965556.26bfb0.3bf7@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-07 22:38:21','Isaac_Obo_Enimil_Cover_Letter_PhotonAI.pdf',NULL);
INSERT INTO "outreaches" VALUES(14,50,30,'hello@celsusos.com','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<6ac6ca1c.09148f95.29b25b.ab88@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-07 22:39:28','Isaac_Obo_Enimil_Cover_Letter_Celsus.pdf',NULL);
INSERT INTO "outreaches" VALUES(15,55,32,'careers@hostnownow.com','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<6ac6ca43.9764b575.346fa8.8679@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-07 22:40:05','Isaac_Obo_Enimil_Cover_Letter_HostNowNow.pdf',NULL);
INSERT INTO "outreaches" VALUES(16,8,6,'info@gammatechgh.com','initial','Forward Deployed / Platform Engineer Application - Isaac Obo Enimil','<6ac6cd38.2243f663.351975.5265@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-07 22:52:42','Isaac_Obo_Enimil_Cover_Letter_Gamma_Technologies.pdf',NULL);
INSERT INTO "outreaches" VALUES(17,9,7,'info@triaxistechnologies.com','initial','Forward Deployed / Platform Engineer Application - Isaac Obo Enimil','<6ac6cd61.a6a2e554.1fbcb4.60b5@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-07 22:53:24','Isaac_Obo_Enimil_Cover_Letter_TriAxis_Technologies.pdf',NULL);
INSERT INTO "outreaches" VALUES(18,11,9,'office@infotypeghana.com','initial','Forward Deployed / Platform Engineer Application - Isaac Obo Enimil','<6ac6cda0.cbade83c.2fc875.c278@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-07 22:54:26','Isaac_Obo_Enimil_Cover_Letter_Infotype_Ghana.pdf',NULL);
INSERT INTO "outreaches" VALUES(19,12,10,'info@zilotechnologies.com','initial','Forward Deployed / Platform Engineer Application - Isaac Obo Enimil','<6ac6cdca.4f27db6c.303b5d.322a@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-07 22:55:08','Isaac_Obo_Enimil_Cover_Letter_Zilo.pdf',NULL);
INSERT INTO "outreaches" VALUES(20,14,11,'info@wantechsolutions.com','initial','Forward Deployed / Platform Engineer Application - Isaac Obo Enimil','<6ac6cdf2.7b11d76c.2f4a6a.ee82@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-07 22:55:48','Isaac_Obo_Enimil_Cover_Letter_Wan_Tech_Solutions.pdf',NULL);
INSERT INTO "outreaches" VALUES(21,16,13,'info@digitsndata.com','initial','Forward Deployed / Platform Engineer Application - Isaac Obo Enimil','<6ac6ce23.3ad7d102.322fb2.9076@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-07 22:56:36','Isaac_Obo_Enimil_Cover_Letter_Digits_&_Data_Limited.pdf',NULL);
INSERT INTO "outreaches" VALUES(22,18,14,'hello@demannytechconsult.com','initial','Forward Deployed / Platform Engineer Application - Isaac Obo Enimil','<6ac6ce4e.b157ee68.1a4fbd.537e@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-07 22:57:21','Isaac_Obo_Enimil_Cover_Letter_De-MannyTech_Consult.pdf',NULL);
INSERT INTO "outreaches" VALUES(23,19,15,'info@mawulikode.com','initial','Forward Deployed / Platform Engineer Application - Isaac Obo Enimil','<6ac6ce81.a9b7157b.3b4a95.597f@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-07 22:58:11','Isaac_Obo_Enimil_Cover_Letter_Mawulikode_Consulting.pdf',NULL);
INSERT INTO "outreaches" VALUES(24,26,17,'teamprogrammers1@gmail.com','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<6ac6cebc.d8747c6a.1fb2f3.fbd1@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-07 22:59:09','Isaac_Obo_Enimil_Cover_Letter_Team_Programmers.pdf',NULL);
INSERT INTO "outreaches" VALUES(25,27,18,'info@samasoftech.net','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<6ac6cefa.a3ebb97f.1075ef.f276@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-07 23:00:12','Isaac_Obo_Enimil_Cover_Letter_Samasoft_Technologies.pdf',NULL);
INSERT INTO "outreaches" VALUES(26,28,19,'emmaktech@gmail.com','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<6ac6cf2b.e25071f0.23431.1a43@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-07 23:01:01','Isaac_Obo_Enimil_Cover_Letter_Emmaktech_Networks.pdf',NULL);
INSERT INTO "outreaches" VALUES(27,34,20,'info@telenet.com.gh','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<6ac6cf67.1a14101c.2ae172.63a5@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-07 23:02:01','Isaac_Obo_Enimil_Cover_Letter_Telenet_Ghana.pdf',NULL);
INSERT INTO "outreaches" VALUES(28,35,21,'info@telesol.com.gh','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<6ac6cfa0.c193e8a6.f1cd3.e3e5@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-07 23:02:57','Isaac_Obo_Enimil_Cover_Letter_Telesol.pdf',NULL);
INSERT INTO "outreaches" VALUES(29,36,22,'info@boldnetgh.com','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<6ac6cfe0.041101f3.828c4.3553@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-07 23:04:03','Isaac_Obo_Enimil_Cover_Letter_Boldnet_Internet_Solutions.pdf',NULL);
INSERT INTO "outreaches" VALUES(30,119,70,'info@4th-ir.com','initial','Forward Deployed Engineer Application - Isaac Obo Enimil','<6ac6d00d.57d8eb23.3c7ded.5a0c@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-07 23:04:47','Isaac_Obo_Enimil_Cover_Letter_4th-IR.pdf',NULL);
INSERT INTO "outreaches" VALUES(31,63,33,'hello@orgmento.com','initial','Forward Deployed / Platform Engineer Application - Isaac Obo Enimil','<6ac78545.a9b7157b.3b4a95.7479@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-08 11:57:58','Isaac_Obo_Enimil_Cover_Letter_Orgmento.pdf',NULL);
INSERT INTO "outreaches" VALUES(32,64,34,'info@teksol.com','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<6ac78585.186d2a7f.2d4754.0bcd@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-08 11:59:02','Isaac_Obo_Enimil_Cover_Letter_TekSol_Limited.pdf',NULL);
INSERT INTO "outreaches" VALUES(33,65,35,'ammeterlabs@gmail.com','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<6ac785ae.7b11d76c.2f4a6a.d566@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-08 11:59:43','Isaac_Obo_Enimil_Cover_Letter_Ammeter_Labs.pdf',NULL);
INSERT INTO "outreaches" VALUES(34,66,36,'info@excedi.com','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<6ac785ec.644fff69.1fb61.53ad@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-08 12:00:46','Isaac_Obo_Enimil_Cover_Letter_Excedi_Limited.pdf',NULL);
INSERT INTO "outreaches" VALUES(35,68,37,'info@medirevs.com','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<6ac78611.3559cd73.440a8.bb53@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-08 12:01:22','Isaac_Obo_Enimil_Cover_Letter_Medirevs.pdf',NULL);
INSERT INTO "outreaches" VALUES(36,72,38,'info@qknowedtech.com','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<6ac78643.31081df4.3ada42.5066@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-08 12:02:12','Isaac_Obo_Enimil_Cover_Letter_QKnow_EdTech.pdf',NULL);
INSERT INTO "outreaches" VALUES(37,74,39,'info@edfrica.com','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<6ac7866a.07fe6c77.130754.43b1@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-08 12:02:52','Isaac_Obo_Enimil_Cover_Letter_Edfrica.pdf',NULL);
INSERT INTO "outreaches" VALUES(38,77,40,'info@syllabusgh.com','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<6ac786b6.58d92066.32e02.5270@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-08 12:04:24','Isaac_Obo_Enimil_Cover_Letter_SyllabusGH.pdf',NULL);
INSERT INTO "outreaches" VALUES(39,79,41,'hello@tudu.africa','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<6ac786e8.1049055a.101bb7.4dd8@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-08 12:04:57','Isaac_Obo_Enimil_Cover_Letter_Tudu_Africa.pdf',NULL);
INSERT INTO "outreaches" VALUES(40,81,42,'info@shopbeta.com.gh','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<6ac7871f.041101f3.828c4.a050@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-08 12:05:52','Isaac_Obo_Enimil_Cover_Letter_Shopbeta.pdf',NULL);
INSERT INTO "outreaches" VALUES(41,82,43,'hello@tezeon.com','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<6ac78759.be657367.43fee.b216@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-08 12:06:51','Isaac_Obo_Enimil_Cover_Letter_Tezeon_Ghana.pdf',NULL);
INSERT INTO "outreaches" VALUES(42,84,44,'info@ghvendors.com','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<6ac78793.a9b7157b.3b4a95.7499@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-08 12:07:49','Isaac_Obo_Enimil_Cover_Letter_GHVENDORS.pdf',NULL);
INSERT INTO "outreaches" VALUES(43,86,45,'recruitment@virtualinfosecafrica.com','initial','Forward Deployed / Platform Engineer Application - Isaac Obo Enimil','<6ac787c1.b7bed76c.16df60.698b@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-08 12:08:36','Isaac_Obo_Enimil_Cover_Letter_Virtual_Infosec_Africa.pdf',NULL);
INSERT INTO "outreaches" VALUES(44,87,46,'info@cyber-hawk.com','initial','Forward Deployed / Platform Engineer Application - Isaac Obo Enimil','<6ac787ed.b62143e1.8ac05.7129@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-08 12:09:18','Isaac_Obo_Enimil_Cover_Letter_CyberHawk.pdf',NULL);
INSERT INTO "outreaches" VALUES(45,88,47,'info@kasazon.com','initial','Forward Deployed / Platform Engineer Application - Isaac Obo Enimil','<6ac78820.041101f3.828c4.e781@mx.google.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-08 12:10:10','Isaac_Obo_Enimil_Cover_Letter_Kasazon_Limited.pdf',NULL);
INSERT INTO "outreaches" VALUES(46,6,172,'richard@devarps.com','initial','Forward Deployed / Platform Engineer Application - Isaac Obo Enimil','<179170043564.3037501.3581053571170284133@gmail.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-11 06:34:01','generated_letters/Isaac_Obo_Enimil_Cover_Letter_Devarps.pdf','Dear Richard,

My name is Isaac Obo Enimil. I''m a Platform Engineer (DevOps) at AmaliTech Services GmbH and a Computer Engineering graduate of KNUST, with the AWS Certified Solutions Architect – Associate and Kubernetes and Cloud Native Associate (KCNA) certifications. Alongside the platform work, I build and ship applied AI systems for clients.

I''d like to be considered for Forward Deployed / Platform Engineer work at Devarps. My CV is attached, along with a cover letter written for Devarps.

Some of my work:
- At Turing I exceeded client KPIs for data accuracy and volume, helping take the team to #1 in dataset quality on client-verified benchmarks; at BoaSoft I shipped a RAG platform built around the client''s own documents.
- I design scalable AWS environments with Terraform and Docker, including a secure multi-tier VPC and modular application layers, so environments are reproducible across clients.
- I implement GitOps delivery with Argo CD, treating Git as the single source of truth for cluster state, and inject runtime credentials from HashiCorp Vault to keep secrets out of images and repositories.

If it''s useful, I''d be glad to have a short call with someone on your team or one of your engineering leads.

Thanks for reading.

Best regards,

Isaac Obo Enimil
Kumasi, Ghana
Phone: +233 59 794 4747
Portfolio: https://ioenimil.me
LinkedIn: https://www.linkedin.com/in/isaacoboenimil/
GitHub: https://github.com/ioenimil
');
INSERT INTO "outreaches" VALUES(47,15,93,'olayiwola@esolutionsghana.com','initial','Forward Deployed / Platform Engineer Application - Isaac Obo Enimil','<179170048772.3037501.10320434390538313456@gmail.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-11 06:34:52','generated_letters/Isaac_Obo_Enimil_Cover_Letter_eSolutions_Consulting.pdf','Dear Olayiwola,

My name is Isaac Obo Enimil. I''m a Platform Engineer (DevOps) at AmaliTech Services GmbH and a Computer Engineering graduate of KNUST, with the AWS Certified Solutions Architect – Associate and Kubernetes and Cloud Native Associate (KCNA) certifications. Alongside the platform work, I build and ship applied AI systems for clients.

I''d like to be considered for Forward Deployed / Platform Engineer work at eSolutions Consulting. My CV is attached, along with a cover letter written for eSolutions Consulting.

Some of my work:
- At Turing I exceeded client KPIs for data accuracy and volume, helping take the team to #1 in dataset quality on client-verified benchmarks; at BoaSoft I shipped a RAG platform built around the client''s own documents.
- I design scalable AWS environments with Terraform and Docker, including a secure multi-tier VPC and modular application layers, so environments are reproducible across clients.
- I implement GitOps delivery with Argo CD, treating Git as the single source of truth for cluster state, and inject runtime credentials from HashiCorp Vault to keep secrets out of images and repositories.

If it''s useful, I''d be glad to have a short call with someone on your team or one of your engineering leads.

Thanks for reading.

Best regards,

Isaac Obo Enimil
Kumasi, Ghana
Phone: +233 59 794 4747
Portfolio: https://ioenimil.me
LinkedIn: https://www.linkedin.com/in/isaacoboenimil/
GitHub: https://github.com/ioenimil
');
INSERT INTO "outreaches" VALUES(48,16,95,'lagbemava@digitsndata.com','initial','Forward Deployed / Platform Engineer Application - Isaac Obo Enimil','<179170052721.3037501.7386009815963117649@gmail.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-11 06:35:31','generated_letters/Isaac_Obo_Enimil_Cover_Letter_Digits_&_Data_Limited.pdf','Dear Lawrence,

My name is Isaac Obo Enimil. I''m a Platform Engineer (DevOps) at AmaliTech Services GmbH and a Computer Engineering graduate of KNUST, with the AWS Certified Solutions Architect – Associate and Kubernetes and Cloud Native Associate (KCNA) certifications. Alongside the platform work, I build and ship applied AI systems for clients.

I''d like to be considered for Forward Deployed / Platform Engineer work at Digits & Data Limited. My CV is attached, along with a cover letter written for Digits & Data Limited.

Some of my work:
- At Turing I exceeded client KPIs for data accuracy and volume, helping take the team to #1 in dataset quality on client-verified benchmarks; at BoaSoft I shipped a RAG platform built around the client''s own documents.
- I design scalable AWS environments with Terraform and Docker, including a secure multi-tier VPC and modular application layers, so environments are reproducible across clients.
- I implement GitOps delivery with Argo CD, treating Git as the single source of truth for cluster state, and inject runtime credentials from HashiCorp Vault to keep secrets out of images and repositories.

If it''s useful, I''d be glad to have a short call with someone on your team or one of your engineering leads.

Thanks for reading.

Best regards,

Isaac Obo Enimil
Kumasi, Ghana
Phone: +233 59 794 4747
Portfolio: https://ioenimil.me
LinkedIn: https://www.linkedin.com/in/isaacoboenimil/
GitHub: https://github.com/ioenimil
');
INSERT INTO "outreaches" VALUES(49,19,98,'mawuli.denteh@mawulikode.com','initial','Forward Deployed / Platform Engineer Application - Isaac Obo Enimil','<179170058710.3037501.11881281349904999060@gmail.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-11 06:36:31','generated_letters/Isaac_Obo_Enimil_Cover_Letter_Mawulikode_Consulting.pdf','Dear Mawuli,

My name is Isaac Obo Enimil. I''m a Platform Engineer (DevOps) at AmaliTech Services GmbH and a Computer Engineering graduate of KNUST, with the AWS Certified Solutions Architect – Associate and Kubernetes and Cloud Native Associate (KCNA) certifications. Alongside the platform work, I build and ship applied AI systems for clients.

I''d like to be considered for Forward Deployed / Platform Engineer work at Mawulikode Consulting. My CV is attached, along with a cover letter written for Mawulikode Consulting.

Some of my work:
- At Turing I exceeded client KPIs for data accuracy and volume, helping take the team to #1 in dataset quality on client-verified benchmarks; at BoaSoft I shipped a RAG platform built around the client''s own documents.
- I design scalable AWS environments with Terraform and Docker, including a secure multi-tier VPC and modular application layers, so environments are reproducible across clients.
- I implement GitOps delivery with Argo CD, treating Git as the single source of truth for cluster state, and inject runtime credentials from HashiCorp Vault to keep secrets out of images and repositories.

If it''s useful, I''d be glad to have a short call with someone on your team or one of your engineering leads.

Thanks for reading.

Best regards,

Isaac Obo Enimil
Kumasi, Ghana
Phone: +233 59 794 4747
Portfolio: https://ioenimil.me
LinkedIn: https://www.linkedin.com/in/isaacoboenimil/
GitHub: https://github.com/ioenimil
');
INSERT INTO "outreaches" VALUES(50,55,108,'ayodeji@hostnownow.com','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<179170064141.3037501.15734506946074129679@gmail.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-11 06:37:24','generated_letters/Isaac_Obo_Enimil_Cover_Letter_HostNowNow.pdf','Dear Ayodeji,

My name is Isaac Obo Enimil. I''m a Platform Engineer (DevOps) at AmaliTech Services GmbH and a Computer Engineering graduate of KNUST, with the AWS Certified Solutions Architect – Associate and Kubernetes and Cloud Native Associate (KCNA) certifications. Alongside the platform work, I build and ship applied AI systems for clients.

I''d like to be considered for Platform & DevOps Engineer work at HostNowNow. My CV is attached, along with a cover letter written for HostNowNow.

Some of my work:
- I provision production-ready AWS infrastructure with Terraform and Docker, including a secure multi-tier VPC and modular application layers.
- I built a cost-optimized Jenkins CI/CD engine with EC2 Spot agents that auto-scale with build queue depth, speeding up developer feedback while cutting compute cost.
- I deployed Prometheus, Loki, Grafana, and Jaeger with self-service dashboards that give developers on-demand insight into their environments and error logs.

If it''s useful, I''d be glad to have a short call with someone on your team or one of your engineering leads.

Thanks for reading.

Best regards,

Isaac Obo Enimil
Kumasi, Ghana
Phone: +233 59 794 4747
Portfolio: https://ioenimil.me
LinkedIn: https://www.linkedin.com/in/isaacoboenimil/
GitHub: https://github.com/ioenimil
');
INSERT INTO "outreaches" VALUES(51,63,113,'patrick.simpe-asante@orgmento.com','initial','Forward Deployed / Platform Engineer Application - Isaac Obo Enimil','<179170069174.3037501.17816584049031501718@gmail.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-11 06:38:15','generated_letters/Isaac_Obo_Enimil_Cover_Letter_Orgmento.pdf','Dear Patrick,

My name is Isaac Obo Enimil. I''m a Platform Engineer (DevOps) at AmaliTech Services GmbH and a Computer Engineering graduate of KNUST, with the AWS Certified Solutions Architect – Associate and Kubernetes and Cloud Native Associate (KCNA) certifications. Alongside the platform work, I build and ship applied AI systems for clients.

I''d like to be considered for Forward Deployed / Platform Engineer work at Orgmento. My CV is attached, along with a cover letter written for Orgmento.

Some of my work:
- At Turing I exceeded client KPIs for data accuracy and volume, helping take the team to #1 in dataset quality on client-verified benchmarks; at BoaSoft I shipped a RAG platform built around the client''s own documents.
- I design scalable AWS environments with Terraform and Docker, including a secure multi-tier VPC and modular application layers, so environments are reproducible across clients.
- I implement GitOps delivery with Argo CD, treating Git as the single source of truth for cluster state, and inject runtime credentials from HashiCorp Vault to keep secrets out of images and repositories.

If it''s useful, I''d be glad to have a short call with someone on your team or one of your engineering leads.

Thanks for reading.

Best regards,

Isaac Obo Enimil
Kumasi, Ghana
Phone: +233 59 794 4747
Portfolio: https://ioenimil.me
LinkedIn: https://www.linkedin.com/in/isaacoboenimil/
GitHub: https://github.com/ioenimil
');
INSERT INTO "outreaches" VALUES(52,86,127,'dlamptey@virtualinfosecafrica.com','initial','Forward Deployed / Platform Engineer Application - Isaac Obo Enimil','<179170073886.3037501.3394407111877149526@gmail.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-11 06:39:03','generated_letters/Isaac_Obo_Enimil_Cover_Letter_Virtual_Infosec_Africa.pdf','Dear Daniel,

My name is Isaac Obo Enimil. I''m a Platform Engineer (DevOps) at AmaliTech Services GmbH and a Computer Engineering graduate of KNUST, with the AWS Certified Solutions Architect – Associate and Kubernetes and Cloud Native Associate (KCNA) certifications. Alongside the platform work, I build and ship applied AI systems for clients.

I''d like to be considered for Forward Deployed / Platform Engineer work at Virtual Infosec Africa. My CV is attached, along with a cover letter written for Virtual Infosec Africa.

Some of my work:
- At Turing I exceeded client KPIs for data accuracy and volume, helping take the team to #1 in dataset quality on client-verified benchmarks; at BoaSoft I shipped a RAG platform built around the client''s own documents.
- I design scalable AWS environments with Terraform and Docker, including a secure multi-tier VPC and modular application layers, so environments are reproducible across clients.
- I implement GitOps delivery with Argo CD, treating Git as the single source of truth for cluster state, and inject runtime credentials from HashiCorp Vault to keep secrets out of images and repositories.

If it''s useful, I''d be glad to have a short call with someone on your team or one of your engineering leads.

Thanks for reading.

Best regards,

Isaac Obo Enimil
Kumasi, Ghana
Phone: +233 59 794 4747
Portfolio: https://ioenimil.me
LinkedIn: https://www.linkedin.com/in/isaacoboenimil/
GitHub: https://github.com/ioenimil
');
INSERT INTO "outreaches" VALUES(53,87,128,'callum@cyber-hawk.com','initial','Forward Deployed / Platform Engineer Application - Isaac Obo Enimil','<179170079621.3037501.2427853285833788469@gmail.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-11 06:40:01','generated_letters/Isaac_Obo_Enimil_Cover_Letter_CyberHawk.pdf','Dear Callum,

My name is Isaac Obo Enimil. I''m a Platform Engineer (DevOps) at AmaliTech Services GmbH and a Computer Engineering graduate of KNUST, with the AWS Certified Solutions Architect – Associate and Kubernetes and Cloud Native Associate (KCNA) certifications. Alongside the platform work, I build and ship applied AI systems for clients.

I''d like to be considered for Forward Deployed / Platform Engineer work at CyberHawk. My CV is attached, along with a cover letter written for CyberHawk.

Some of my work:
- At Turing I exceeded client KPIs for data accuracy and volume, helping take the team to #1 in dataset quality on client-verified benchmarks; at BoaSoft I shipped a RAG platform built around the client''s own documents.
- I design scalable AWS environments with Terraform and Docker, including a secure multi-tier VPC and modular application layers, so environments are reproducible across clients.
- I implement GitOps delivery with Argo CD, treating Git as the single source of truth for cluster state, and inject runtime credentials from HashiCorp Vault to keep secrets out of images and repositories.

If it''s useful, I''d be glad to have a short call with someone on your team or one of your engineering leads.

Thanks for reading.

Best regards,

Isaac Obo Enimil
Kumasi, Ghana
Phone: +233 59 794 4747
Portfolio: https://ioenimil.me
LinkedIn: https://www.linkedin.com/in/isaacoboenimil/
GitHub: https://github.com/ioenimil
');
INSERT INTO "outreaches" VALUES(54,89,130,'olusola@bochsystems.net','initial','Forward Deployed / Platform Engineer Application - Isaac Obo Enimil','<179170085819.3037501.14675018528112246148@gmail.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-11 06:41:01','generated_letters/Isaac_Obo_Enimil_Cover_Letter_Boch_Systems_Ghana.pdf','Dear Olusola,

My name is Isaac Obo Enimil. I''m a Platform Engineer (DevOps) at AmaliTech Services GmbH and a Computer Engineering graduate of KNUST, with the AWS Certified Solutions Architect – Associate and Kubernetes and Cloud Native Associate (KCNA) certifications. Alongside the platform work, I build and ship applied AI systems for clients.

I''d like to be considered for Forward Deployed / Platform Engineer work at Boch Systems Ghana. My CV is attached, along with a cover letter written for Boch Systems Ghana.

Some of my work:
- At Turing I exceeded client KPIs for data accuracy and volume, helping take the team to #1 in dataset quality on client-verified benchmarks; at BoaSoft I shipped a RAG platform built around the client''s own documents.
- I design scalable AWS environments with Terraform and Docker, including a secure multi-tier VPC and modular application layers, so environments are reproducible across clients.
- I implement GitOps delivery with Argo CD, treating Git as the single source of truth for cluster state, and inject runtime credentials from HashiCorp Vault to keep secrets out of images and repositories.

If it''s useful, I''d be glad to have a short call with someone on your team or one of your engineering leads.

Thanks for reading.

Best regards,

Isaac Obo Enimil
Kumasi, Ghana
Phone: +233 59 794 4747
Portfolio: https://ioenimil.me
LinkedIn: https://www.linkedin.com/in/isaacoboenimil/
GitHub: https://github.com/ioenimil
');
INSERT INTO "outreaches" VALUES(55,102,145,'nayram@myfigtech.com','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<179170091157.3037501.18181087289016164865@gmail.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-11 06:41:55','generated_letters/Isaac_Obo_Enimil_Cover_Letter_Figtech.pdf','Dear Nayram,

My name is Isaac Obo Enimil. I''m a Platform Engineer (DevOps) at AmaliTech Services GmbH and a Computer Engineering graduate of KNUST, with the AWS Certified Solutions Architect – Associate and Kubernetes and Cloud Native Associate (KCNA) certifications. Alongside the platform work, I build and ship applied AI systems for clients.

I''d like to be considered for Platform & DevOps Engineer work at Figtech. My CV is attached, along with a cover letter written for Figtech.

Some of my work:
- I won 1st place at the KNUST Technology Week Hackathon with a containerized remittance platform using Kafka for event streaming, a secure API gateway, an ACID-compliant orchestrator, and immutable audit logging.
- I engineered a cost-optimized Jenkins pipeline with auto-scaling EC2 Spot agents, and secured a Jenkins setup for 10 developers with Keycloak SSO and RBAC across 5 cross-functional teams.
- I deployed Prometheus, Thanos, Loki, Grafana, and Jaeger with distributed tracing and automated alerting, reducing Mean Time To Resolution (MTTR).

If it''s useful, I''d be glad to have a short call with someone on your team or one of your engineering leads.

Thanks for reading.

Best regards,

Isaac Obo Enimil
Kumasi, Ghana
Phone: +233 59 794 4747
Portfolio: https://ioenimil.me
LinkedIn: https://www.linkedin.com/in/isaacoboenimil/
GitHub: https://github.com/ioenimil
');
INSERT INTO "outreaches" VALUES(56,103,146,'david@getdaabo.com','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<179170096124.3037501.8984996519551038600@gmail.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-11 06:42:46','generated_letters/Isaac_Obo_Enimil_Cover_Letter_Daabo.pdf','Dear David,

My name is Isaac Obo Enimil. I''m a Platform Engineer (DevOps) at AmaliTech Services GmbH and a Computer Engineering graduate of KNUST, with the AWS Certified Solutions Architect – Associate and Kubernetes and Cloud Native Associate (KCNA) certifications. Alongside the platform work, I build and ship applied AI systems for clients.

I''d like to be considered for Platform & DevOps Engineer work at Daabo. My CV is attached, along with a cover letter written for Daabo.

Some of my work:
- I won 1st place at the KNUST Technology Week Hackathon with a containerized remittance platform using Kafka for event streaming, a secure API gateway, an ACID-compliant orchestrator, and immutable audit logging.
- I engineered a cost-optimized Jenkins pipeline with auto-scaling EC2 Spot agents, and secured a Jenkins setup for 10 developers with Keycloak SSO and RBAC across 5 cross-functional teams.
- I deployed Prometheus, Thanos, Loki, Grafana, and Jaeger with distributed tracing and automated alerting, reducing Mean Time To Resolution (MTTR).

If it''s useful, I''d be glad to have a short call with someone on your team or one of your engineering leads.

Thanks for reading.

Best regards,

Isaac Obo Enimil
Kumasi, Ghana
Phone: +233 59 794 4747
Portfolio: https://ioenimil.me
LinkedIn: https://www.linkedin.com/in/isaacoboenimil/
GitHub: https://github.com/ioenimil
');
INSERT INTO "outreaches" VALUES(57,104,147,'alfred@ridewithmaya.com','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<179170099842.3037501.17402467102504477316@gmail.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-11 06:43:21','generated_letters/Isaac_Obo_Enimil_Cover_Letter_Maya.pdf','Dear Alfred,

My name is Isaac Obo Enimil. I''m a Platform Engineer (DevOps) at AmaliTech Services GmbH and a Computer Engineering graduate of KNUST, with the AWS Certified Solutions Architect – Associate and Kubernetes and Cloud Native Associate (KCNA) certifications. Alongside the platform work, I build and ship applied AI systems for clients.

I''d like to be considered for Platform & DevOps Engineer work at Maya. My CV is attached, along with a cover letter written for Maya.

Some of my work:
- I provision production-ready AWS infrastructure with Terraform and Docker, including a secure multi-tier VPC and modular application layers.
- I built a cost-optimized Jenkins CI/CD engine with EC2 Spot agents that auto-scale with build queue depth, speeding up developer feedback while cutting compute cost.
- I deployed Prometheus, Loki, Grafana, and Jaeger with self-service dashboards that give developers on-demand insight into their environments and error logs.

If it''s useful, I''d be glad to have a short call with someone on your team or one of your engineering leads.

Thanks for reading.

Best regards,

Isaac Obo Enimil
Kumasi, Ghana
Phone: +233 59 794 4747
Portfolio: https://ioenimil.me
LinkedIn: https://www.linkedin.com/in/isaacoboenimil/
GitHub: https://github.com/ioenimil
');
INSERT INTO "outreaches" VALUES(58,106,79,'samuel.aggrey@completefarmer.com','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<179170103893.3037501.7491606138005022851@gmail.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-11 06:44:04','generated_letters/Isaac_Obo_Enimil_Cover_Letter_Complete_Farmer.pdf','Dear Samuel,

My name is Isaac Obo Enimil. I''m a Platform Engineer (DevOps) at AmaliTech Services GmbH and a Computer Engineering graduate of KNUST, with the AWS Certified Solutions Architect – Associate and Kubernetes and Cloud Native Associate (KCNA) certifications. Alongside the platform work, I build and ship applied AI systems for clients.

I''d like to be considered for Platform & DevOps Engineer work at Complete Farmer. My CV is attached, along with a cover letter written for Complete Farmer.

Some of my work:
- I provision production-ready AWS infrastructure with Terraform and Docker, including a secure multi-tier VPC and modular application layers.
- I built a cost-optimized Jenkins CI/CD engine with EC2 Spot agents that auto-scale with build queue depth, speeding up developer feedback while cutting compute cost.
- I deployed Prometheus, Loki, Grafana, and Jaeger with self-service dashboards that give developers on-demand insight into their environments and error logs.

If it''s useful, I''d be glad to have a short call with someone on your team or one of your engineering leads.

Thanks for reading.

Best regards,

Isaac Obo Enimil
Kumasi, Ghana
Phone: +233 59 794 4747
Portfolio: https://ioenimil.me
LinkedIn: https://www.linkedin.com/in/isaacoboenimil/
GitHub: https://github.com/ioenimil
');
INSERT INTO "outreaches" VALUES(59,117,159,'joybonsuschmutz@abeyiestudios.com','initial','Forward Deployed / Platform Engineer Application - Isaac Obo Enimil','<179170107532.3037501.5796719530741785303@gmail.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-11 06:44:40','generated_letters/Isaac_Obo_Enimil_Cover_Letter_Abeyie_Innovation_Studios.pdf','Dear Joy,

My name is Isaac Obo Enimil. I''m a Platform Engineer (DevOps) at AmaliTech Services GmbH and a Computer Engineering graduate of KNUST, with the AWS Certified Solutions Architect – Associate and Kubernetes and Cloud Native Associate (KCNA) certifications. Alongside the platform work, I build and ship applied AI systems for clients.

I''d like to be considered for Forward Deployed / Platform Engineer work at Abeyie Innovation Studios. My CV is attached, along with a cover letter written for Abeyie Innovation Studios.

Some of my work:
- At Turing I exceeded client KPIs for data accuracy and volume, helping take the team to #1 in dataset quality on client-verified benchmarks; at BoaSoft I shipped a RAG platform built around the client''s own documents.
- I design scalable AWS environments with Terraform and Docker, including a secure multi-tier VPC and modular application layers, so environments are reproducible across clients.
- I implement GitOps delivery with Argo CD, treating Git as the single source of truth for cluster state, and inject runtime credentials from HashiCorp Vault to keep secrets out of images and repositories.

If it''s useful, I''d be glad to have a short call with someone on your team or one of your engineering leads.

Thanks for reading.

Best regards,

Isaac Obo Enimil
Kumasi, Ghana
Phone: +233 59 794 4747
Portfolio: https://ioenimil.me
LinkedIn: https://www.linkedin.com/in/isaacoboenimil/
GitHub: https://github.com/ioenimil
');
INSERT INTO "outreaches" VALUES(60,119,170,'z.khalid@4th-ir.com','initial','Forward Deployed Engineer Application - Isaac Obo Enimil','<179170112336.3037501.3584974764132303153@gmail.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-11 06:45:27','generated_letters/Isaac_Obo_Enimil_Cover_Letter_4th-IR.pdf','Dear Zeeshan,

My name is Isaac Obo Enimil. I''m a Platform Engineer (DevOps) at AmaliTech Services GmbH and a Computer Engineering graduate of KNUST, with the AWS Certified Solutions Architect – Associate and Kubernetes and Cloud Native Associate (KCNA) certifications. Alongside the platform work, I build and ship applied AI systems for clients.

I''d like to be considered for Forward Deployed Engineer work at 4th-IR. My CV is attached, along with a cover letter written for 4th-IR.

Some of my work:
- I built an end-to-end RAG system with FastAPI and the Zilliz vector store, grounding answers in a client''s verified documents, with a serverless ingestion pipeline and a React frontend for context-aware document interrogation.
- I architected a natural-language analytics agent on CopilotKit and Cube Core, and used a DeepEval golden dataset to raise output reliability from 74% to 96% by constraining queries to declared measures and dimensions.
- I run containerized workloads on production Kubernetes with GitOps delivery via Argo CD, secrets from HashiCorp Vault, and Prometheus, Loki, Grafana, and Jaeger observability, so what I ship stays running.

If it''s useful, I''d be glad to have a short call with someone on your team or one of your engineering leads.

Thanks for reading.

Best regards,

Isaac Obo Enimil
Kumasi, Ghana
Phone: +233 59 794 4747
Portfolio: https://ioenimil.me
LinkedIn: https://www.linkedin.com/in/isaacoboenimil/
GitHub: https://github.com/ioenimil
');
INSERT INTO "outreaches" VALUES(61,122,221,'keerthana@zethic.com','initial','Forward Deployed / Platform Engineer Application - Isaac Obo Enimil','<179204813792.1425796.9435455301089754457@gmail.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-15 07:09:03','generated_letters/Isaac_Obo_Enimil_Cover_Letter_Zethic.pdf','Dear Keerthana,

My name is Isaac Obo Enimil. I''m a Platform Engineer (DevOps) at AmaliTech Services GmbH and a Computer Engineering graduate of KNUST, with the AWS Certified Solutions Architect – Associate and Kubernetes and Cloud Native Associate (KCNA) certifications. Alongside the platform work, I build and ship applied AI systems for clients.

I''d like to be considered for Forward Deployed / Platform Engineer work at Zethic. My CV is attached, along with a cover letter written for Zethic.

Some of my work:
- At Turing I exceeded client KPIs for data accuracy and volume, helping take the team to #1 in dataset quality on client-verified benchmarks; at BoaSoft I shipped a RAG platform built around the client''s own documents.
- I design scalable AWS environments with Terraform and Docker, including a secure multi-tier VPC and modular application layers, so environments are reproducible across clients.
- I implement GitOps delivery with Argo CD, treating Git as the single source of truth for cluster state, and inject runtime credentials from HashiCorp Vault to keep secrets out of images and repositories.

If it''s useful, I''d be glad to have a short call with someone on your team or one of your engineering leads.

Thanks for reading.

Best regards,

Isaac Obo Enimil
Kumasi, Ghana
Phone: +233 59 794 4747
Portfolio: https://ioenimil.me
LinkedIn: https://www.linkedin.com/in/isaacoboenimil/
GitHub: https://github.com/ioenimil
');
INSERT INTO "outreaches" VALUES(62,123,194,'niitetteh@expresspaygh.com','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<179204817594.1425796.16252720055564665715@gmail.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-15 07:09:41','generated_letters/Isaac_Obo_Enimil_Cover_Letter_expressPay_Ghana.pdf','Dear Nii,

My name is Isaac Obo Enimil. I''m a Platform Engineer (DevOps) at AmaliTech Services GmbH and a Computer Engineering graduate of KNUST, with the AWS Certified Solutions Architect – Associate and Kubernetes and Cloud Native Associate (KCNA) certifications. Alongside the platform work, I build and ship applied AI systems for clients.

I''d like to be considered for Platform & DevOps Engineer work at expressPay Ghana. My CV is attached, along with a cover letter written for expressPay Ghana.

Some of my work:
- I won 1st place at the KNUST Technology Week Hackathon with a containerized remittance platform using Kafka for event streaming, a secure API gateway, an ACID-compliant orchestrator, and immutable audit logging.
- I engineered a cost-optimized Jenkins pipeline with auto-scaling EC2 Spot agents, and secured a Jenkins setup for 10 developers with Keycloak SSO and RBAC across 5 cross-functional teams.
- I deployed Prometheus, Thanos, Loki, Grafana, and Jaeger with distributed tracing and automated alerting, reducing Mean Time To Resolution (MTTR).

If it''s useful, I''d be glad to have a short call with someone on your team or one of your engineering leads.

Thanks for reading.

Best regards,

Isaac Obo Enimil
Kumasi, Ghana
Phone: +233 59 794 4747
Portfolio: https://ioenimil.me
LinkedIn: https://www.linkedin.com/in/isaacoboenimil/
GitHub: https://github.com/ioenimil
');
INSERT INTO "outreaches" VALUES(63,124,175,'calvin.thomas@turntabl.io','initial','Forward Deployed / Platform Engineer Application - Isaac Obo Enimil','<179204821706.1425796.17214502029795349139@gmail.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-15 07:10:21','generated_letters/Isaac_Obo_Enimil_Cover_Letter_turntabl.pdf','Dear Calvin,

My name is Isaac Obo Enimil. I''m a Platform Engineer (DevOps) at AmaliTech Services GmbH and a Computer Engineering graduate of KNUST, with the AWS Certified Solutions Architect – Associate and Kubernetes and Cloud Native Associate (KCNA) certifications. Alongside the platform work, I build and ship applied AI systems for clients.

I''d like to be considered for Forward Deployed / Platform Engineer work at turntabl. My CV is attached, along with a cover letter written for turntabl.

Some of my work:
- At Turing I exceeded client KPIs for data accuracy and volume, helping take the team to #1 in dataset quality on client-verified benchmarks; at BoaSoft I shipped a RAG platform built around the client''s own documents.
- I design scalable AWS environments with Terraform and Docker, including a secure multi-tier VPC and modular application layers, so environments are reproducible across clients.
- I implement GitOps delivery with Argo CD, treating Git as the single source of truth for cluster state, and inject runtime credentials from HashiCorp Vault to keep secrets out of images and repositories.

If it''s useful, I''d be glad to have a short call with someone on your team or one of your engineering leads.

Thanks for reading.

Best regards,

Isaac Obo Enimil
Kumasi, Ghana
Phone: +233 59 794 4747
Portfolio: https://ioenimil.me
LinkedIn: https://www.linkedin.com/in/isaacoboenimil/
GitHub: https://github.com/ioenimil
');
INSERT INTO "outreaches" VALUES(64,126,219,'matt.machuga@oysterhr.com','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil',NULL,NULL,NULL,'FAILED','[Errno -2] Name or service not known','2026-10-15 07:11:43','generated_letters/Isaac_Obo_Enimil_Cover_Letter_Oyster.pdf','Dear Matt,

My name is Isaac Obo Enimil. I''m a Platform Engineer (DevOps) at AmaliTech Services GmbH and a Computer Engineering graduate of KNUST, with the AWS Certified Solutions Architect – Associate and Kubernetes and Cloud Native Associate (KCNA) certifications. Alongside the platform work, I build and ship applied AI systems for clients.

I''d like to be considered for Platform & DevOps Engineer work at Oyster. My CV is attached, along with a cover letter written for Oyster.

Some of my work:
- I provision production-ready AWS infrastructure with Terraform and Docker, including a secure multi-tier VPC and modular application layers.
- I built a cost-optimized Jenkins CI/CD engine with EC2 Spot agents that auto-scale with build queue depth, speeding up developer feedback while cutting compute cost.
- I deployed Prometheus, Loki, Grafana, and Jaeger with self-service dashboards that give developers on-demand insight into their environments and error logs.

If it''s useful, I''d be glad to have a short call with someone on your team or one of your engineering leads.

Thanks for reading.

Best regards,

Isaac Obo Enimil
Kumasi, Ghana
Phone: +233 59 794 4747
Portfolio: https://ioenimil.me
LinkedIn: https://www.linkedin.com/in/isaacoboenimil/
GitHub: https://github.com/ioenimil
');
INSERT INTO "outreaches" VALUES(65,127,208,'molly@protocol.ai','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<179204834619.1425796.8269088106577005755@gmail.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-15 07:12:32','generated_letters/Isaac_Obo_Enimil_Cover_Letter_Protocol_Labs.pdf','Dear Molly,

My name is Isaac Obo Enimil. I''m a Platform Engineer (DevOps) at AmaliTech Services GmbH and a Computer Engineering graduate of KNUST, with the AWS Certified Solutions Architect – Associate and Kubernetes and Cloud Native Associate (KCNA) certifications. Alongside the platform work, I build and ship applied AI systems for clients.

I''d like to be considered for Platform & DevOps Engineer work at Protocol Labs. My CV is attached, along with a cover letter written for Protocol Labs.

Some of my work:
- I provision production-ready AWS infrastructure with Terraform and Docker, including a secure multi-tier VPC and modular application layers.
- I built a cost-optimized Jenkins CI/CD engine with EC2 Spot agents that auto-scale with build queue depth, speeding up developer feedback while cutting compute cost.
- I deployed Prometheus, Loki, Grafana, and Jaeger with self-service dashboards that give developers on-demand insight into their environments and error logs.

If it''s useful, I''d be glad to have a short call with someone on your team or one of your engineering leads.

Thanks for reading.

Best regards,

Isaac Obo Enimil
Kumasi, Ghana
Phone: +233 59 794 4747
Portfolio: https://ioenimil.me
LinkedIn: https://www.linkedin.com/in/isaacoboenimil/
GitHub: https://github.com/ioenimil
');
INSERT INTO "outreaches" VALUES(66,43,25,'michael.ofeor@niiosalabs.com','followup','Re: Forward Deployed Engineer Application - Isaac Obo Enimil','<179204847733.1431726.12393083362217520277@gmail.com>','<6ac6c987.75747b7c.ea71c.40ac@mx.google.com>','<6ac6c987.75747b7c.ea71c.40ac@mx.google.com>','SUCCESS',NULL,'2026-10-15 07:14:40',NULL,'Dear NiiOsa Labs team,

A quick follow-up on my earlier note about Forward Deployed Engineer work at NiiOsa Labs.

I''m still keen. If there''s an opening, or a 10-minute call would be easier than email, I''m happy to work around your schedule. The short version of what I''d bring: platform engineering on AWS and Kubernetes, GitOps delivery, observability, and applied AI shipped for clients.

My CV is attached again so you don''t have to dig for it.

Best regards,

Isaac Obo Enimil
Kumasi, Ghana
Phone: +233 59 794 4747
Portfolio: https://ioenimil.me
LinkedIn: https://www.linkedin.com/in/isaacoboenimil/
GitHub: https://github.com/ioenimil
');
INSERT INTO "outreaches" VALUES(67,126,219,'matt.machuga@oysterhr.com','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<179204849730.1435300.4203993246667005875@gmail.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-15 07:15:02','generated_letters/Isaac_Obo_Enimil_Cover_Letter_Oyster.pdf','Dear Matt,

My name is Isaac Obo Enimil. I''m a Platform Engineer (DevOps) at AmaliTech Services GmbH and a Computer Engineering graduate of KNUST, with the AWS Certified Solutions Architect – Associate and Kubernetes and Cloud Native Associate (KCNA) certifications. Alongside the platform work, I build and ship applied AI systems for clients.

I''d like to be considered for Platform & DevOps Engineer work at Oyster. My CV is attached, along with a cover letter written for Oyster.

Some of my work:
- I provision production-ready AWS infrastructure with Terraform and Docker, including a secure multi-tier VPC and modular application layers.
- I built a cost-optimized Jenkins CI/CD engine with EC2 Spot agents that auto-scale with build queue depth, speeding up developer feedback while cutting compute cost.
- I deployed Prometheus, Loki, Grafana, and Jaeger with self-service dashboards that give developers on-demand insight into their environments and error logs.

If it''s useful, I''d be glad to have a short call with someone on your team or one of your engineering leads.

Thanks for reading.

Best regards,

Isaac Obo Enimil
Kumasi, Ghana
Phone: +233 59 794 4747
Portfolio: https://ioenimil.me
LinkedIn: https://www.linkedin.com/in/isaacoboenimil/
GitHub: https://github.com/ioenimil
');
INSERT INTO "outreaches" VALUES(68,96,139,'henry.baffoe@bigdataghana.com','initial','Forward Deployed / Platform Engineer Application - Isaac Obo Enimil','<179205049392.1488564.9137220264078081753@gmail.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-15 07:48:19','generated_letters/Isaac_Obo_Enimil_Cover_Letter_BigData_Ghana.pdf','Dear Henry,

My name is Isaac Obo Enimil. I''m a Platform Engineer (DevOps) at AmaliTech Services GmbH and a Computer Engineering graduate of KNUST, with the AWS Certified Solutions Architect – Associate and Kubernetes and Cloud Native Associate (KCNA) certifications. Alongside the platform work, I build and ship applied AI systems for clients.

I''d like to be considered for Forward Deployed / Platform Engineer work at BigData Ghana. My CV is attached, along with a cover letter written for BigData Ghana.

Some of my work:
- At Turing I exceeded client KPIs for data accuracy and volume, helping take the team to #1 in dataset quality on client-verified benchmarks; at BoaSoft I shipped a RAG platform built around the client''s own documents.
- I design scalable AWS environments with Terraform and Docker, including a secure multi-tier VPC and modular application layers, so environments are reproducible across clients.
- I implement GitOps delivery with Argo CD, treating Git as the single source of truth for cluster state, and inject runtime credentials from HashiCorp Vault to keep secrets out of images and repositories.

If it''s useful, I''d be glad to have a short call with someone on your team or one of your engineering leads.

Thanks for reading.

Best regards,

Isaac Obo Enimil
Kumasi, Ghana
Phone: +233 59 794 4747
Portfolio: https://ioenimil.me
LinkedIn: https://www.linkedin.com/in/isaacoboenimil/
GitHub: https://github.com/ioenimil
');
INSERT INTO "outreaches" VALUES(69,109,152,'isaac@sesitechnologies.com','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<179205053367.1488564.7399074528158371373@gmail.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-15 07:48:58','generated_letters/Isaac_Obo_Enimil_Cover_Letter_Sesi_Technologies.pdf','Dear Isaac,

My name is Isaac Obo Enimil. I''m a Platform Engineer (DevOps) at AmaliTech Services GmbH and a Computer Engineering graduate of KNUST, with the AWS Certified Solutions Architect – Associate and Kubernetes and Cloud Native Associate (KCNA) certifications. Alongside the platform work, I build and ship applied AI systems for clients.

I''d like to be considered for Platform & DevOps Engineer work at Sesi Technologies. My CV is attached, along with a cover letter written for Sesi Technologies.

Some of my work:
- I provision production-ready AWS infrastructure with Terraform and Docker, including a secure multi-tier VPC and modular application layers.
- I built a cost-optimized Jenkins CI/CD engine with EC2 Spot agents that auto-scale with build queue depth, speeding up developer feedback while cutting compute cost.
- I deployed Prometheus, Loki, Grafana, and Jaeger with self-service dashboards that give developers on-demand insight into their environments and error logs.

If it''s useful, I''d be glad to have a short call with someone on your team or one of your engineering leads.

Thanks for reading.

Best regards,

Isaac Obo Enimil
Kumasi, Ghana
Phone: +233 59 794 4747
Portfolio: https://ioenimil.me
LinkedIn: https://www.linkedin.com/in/isaacoboenimil/
GitHub: https://github.com/ioenimil
');
INSERT INTO "outreaches" VALUES(70,129,232,'will@withboost.co','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<179205059872.1488564.792536724121671775@gmail.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-15 07:50:02','generated_letters/Isaac_Obo_Enimil_Cover_Letter_Boost.pdf','Dear Will,

My name is Isaac Obo Enimil. I''m a Platform Engineer (DevOps) at AmaliTech Services GmbH and a Computer Engineering graduate of KNUST, with the AWS Certified Solutions Architect – Associate and Kubernetes and Cloud Native Associate (KCNA) certifications. Alongside the platform work, I build and ship applied AI systems for clients.

I''d like to be considered for Platform & DevOps Engineer work at Boost. My CV is attached, along with a cover letter written for Boost.

Some of my work:
- I provision production-ready AWS infrastructure with Terraform and Docker, including a secure multi-tier VPC and modular application layers.
- I built a cost-optimized Jenkins CI/CD engine with EC2 Spot agents that auto-scale with build queue depth, speeding up developer feedback while cutting compute cost.
- I deployed Prometheus, Loki, Grafana, and Jaeger with self-service dashboards that give developers on-demand insight into their environments and error logs.

If it''s useful, I''d be glad to have a short call with someone on your team or one of your engineering leads.

Thanks for reading.

Best regards,

Isaac Obo Enimil
Kumasi, Ghana
Phone: +233 59 794 4747
Portfolio: https://ioenimil.me
LinkedIn: https://www.linkedin.com/in/isaacoboenimil/
GitHub: https://github.com/ioenimil
');
INSERT INTO "outreaches" VALUES(71,132,239,'kevin@bitovi.com','initial','Forward Deployed / Platform Engineer Application - Isaac Obo Enimil','<179205064473.1488564.5050657526624140056@gmail.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-15 07:50:48','generated_letters/Isaac_Obo_Enimil_Cover_Letter_Bitovi.pdf','Dear Kevin,

My name is Isaac Obo Enimil. I''m a Platform Engineer (DevOps) at AmaliTech Services GmbH and a Computer Engineering graduate of KNUST, with the AWS Certified Solutions Architect – Associate and Kubernetes and Cloud Native Associate (KCNA) certifications. Alongside the platform work, I build and ship applied AI systems for clients.

I''d like to be considered for Forward Deployed / Platform Engineer work at Bitovi. My CV is attached, along with a cover letter written for Bitovi.

Some of my work:
- At Turing I exceeded client KPIs for data accuracy and volume, helping take the team to #1 in dataset quality on client-verified benchmarks; at BoaSoft I shipped a RAG platform built around the client''s own documents.
- I design scalable AWS environments with Terraform and Docker, including a secure multi-tier VPC and modular application layers, so environments are reproducible across clients.
- I implement GitOps delivery with Argo CD, treating Git as the single source of truth for cluster state, and inject runtime credentials from HashiCorp Vault to keep secrets out of images and repositories.

If it''s useful, I''d be glad to have a short call with someone on your team or one of your engineering leads.

Thanks for reading.

Best regards,

Isaac Obo Enimil
Kumasi, Ghana
Phone: +233 59 794 4747
Portfolio: https://ioenimil.me
LinkedIn: https://www.linkedin.com/in/isaacoboenimil/
GitHub: https://github.com/ioenimil
');
INSERT INTO "outreaches" VALUES(72,133,249,'stuart@openfn.org','initial','Platform & DevOps Engineer Application - Isaac Obo Enimil','<179205068881.1488564.17080974193168705288@gmail.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-15 07:51:32','generated_letters/Isaac_Obo_Enimil_Cover_Letter_OpenFn.pdf','Dear Stuart,

My name is Isaac Obo Enimil. I''m a Platform Engineer (DevOps) at AmaliTech Services GmbH and a Computer Engineering graduate of KNUST, with the AWS Certified Solutions Architect – Associate and Kubernetes and Cloud Native Associate (KCNA) certifications. Alongside the platform work, I build and ship applied AI systems for clients.

I''d like to be considered for Platform & DevOps Engineer work at OpenFn. My CV is attached, along with a cover letter written for OpenFn.

Some of my work:
- I provision production-ready AWS infrastructure with Terraform and Docker, including a secure multi-tier VPC and modular application layers.
- I built a cost-optimized Jenkins CI/CD engine with EC2 Spot agents that auto-scale with build queue depth, speeding up developer feedback while cutting compute cost.
- I deployed Prometheus, Loki, Grafana, and Jaeger with self-service dashboards that give developers on-demand insight into their environments and error logs.

If it''s useful, I''d be glad to have a short call with someone on your team or one of your engineering leads.

Thanks for reading.

Best regards,

Isaac Obo Enimil
Kumasi, Ghana
Phone: +233 59 794 4747
Portfolio: https://ioenimil.me
LinkedIn: https://www.linkedin.com/in/isaacoboenimil/
GitHub: https://github.com/ioenimil
');
INSERT INTO "outreaches" VALUES(73,137,264,'kofi@acsint.io','initial','Forward Deployed / Platform Engineer Application - Isaac Obo Enimil','<179210265439.1431946.15891287466330034320@gmail.com>',NULL,NULL,'SUCCESS',NULL,'2026-10-15 22:17:38','generated_letters/Isaac_Obo_Enimil_Cover_Letter_Adaptive_Computer_Solutions_(ACS_Ghana).pdf','Dear Nana Kofi,

My name is Isaac Obo Enimil. I''m a Platform Engineer (DevOps) at AmaliTech Services GmbH and a Computer Engineering graduate of KNUST, with the AWS Certified Solutions Architect – Associate and Kubernetes and Cloud Native Associate (KCNA) certifications. Alongside the platform work, I build and ship applied AI systems for clients.

I''d like to be considered for Forward Deployed / Platform Engineer work at Adaptive Computer Solutions (ACS Ghana). My CV is attached, along with a cover letter written for Adaptive Computer Solutions (ACS Ghana).

Some of my work:
- At Turing I exceeded client KPIs for data accuracy and volume, helping take the team to #1 in dataset quality on client-verified benchmarks; at BoaSoft I shipped a RAG platform built around the client''s own documents.
- I design scalable AWS environments with Terraform and Docker, including a secure multi-tier VPC and modular application layers, so environments are reproducible across clients.
- I implement GitOps delivery with Argo CD, treating Git as the single source of truth for cluster state, and inject runtime credentials from HashiCorp Vault to keep secrets out of images and repositories.

If it''s useful, I''d be glad to have a short call with someone on your team or one of your engineering leads.

Thanks for reading.

Best regards,

Isaac Obo Enimil
Kumasi, Ghana
Phone: +233 59 794 4747
Portfolio: https://ioenimil.me
LinkedIn: https://www.linkedin.com/in/isaacoboenimil/
GitHub: https://github.com/ioenimil
');
CREATE TABLE people (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
        full_name TEXT NOT NULL COLLATE NOCASE,
        title TEXT,
        profile_url TEXT,
        source TEXT CHECK(source IS NULL OR source IN ('exa', 'hunter', 'prospeo', 'manual')),
        contact_id INTEGER REFERENCES contacts(id) ON DELETE SET NULL,
        created_at TEXT,
        UNIQUE(company_id, full_name)
    );
INSERT INTO "people" VALUES(1,1,'Ebo Mensah','Chief Technology Officer','https://pepapay.com/','exa',NULL,'2026-10-11 05:23:10');
INSERT INTO "people" VALUES(2,1,'Priscilla Adjei','Head of People','https://pepapay.com/','exa',NULL,'2026-10-11 05:23:10');
INSERT INTO "people" VALUES(3,1,'Kojo Owusu','Co-founder & CEO','https://pepapay.com/','exa',NULL,'2026-10-11 05:23:10');
INSERT INTO "people" VALUES(4,1,'Akua Asare','Co-founder & COO','https://pepapay.com/','exa',NULL,'2026-10-11 05:23:10');
INSERT INTO "people" VALUES(5,3,'Gati Blaise Makafui','Chief Technology Officer','https://dodystack.com/portfolio','exa',NULL,'2026-10-11 05:32:26');
INSERT INTO "people" VALUES(6,3,'Glister Baffoe','Co-Founder','https://dodystack.com/portfolio','exa',NULL,'2026-10-11 05:32:26');
INSERT INTO "people" VALUES(7,3,'Kenneth Ofosu Antwi','Chief Executive Officer','https://linkedin.com/in/kenneth-ofosu-antwi-3010a6166','exa',NULL,'2026-10-11 05:32:26');
INSERT INTO "people" VALUES(8,6,'Richard Bunnah','Founder & CEO','https://www.devarps.com/about','exa',NULL,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(9,8,'Iakovos Papadimitriou','Chief Technology Officer','https://linkedin.com/in/iakovos-papadimitriou-46b3871','exa',NULL,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(10,8,'Milana Cook','Senior R&D Director, UI and Software Development / Head Of Software Development','https://linkedin.com/in/milana-cook-a387a01b9','exa',NULL,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(11,8,'Dimple Shah','President and Chief Executive Officer','https://people.equilar.com/bio/person/dimple-shah-gamma-technologies/45686812','exa',NULL,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(12,8,'Tom Morel','Founder, Chairman of the Board','https://streamline.gtisoft.com/leadership-team/','exa',NULL,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(13,8,'Syed Wahiduzzaman','Founder, Senior Vice President','https://streamline.gtisoft.com/leadership-team/','exa',NULL,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(14,8,'Rifat Keribar','Founder, Corporate Fellow','https://people.equilar.com/bio/person/rifat-keribar-gamma-technologies/74555635','exa',NULL,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(15,9,'Ajith Kumar','CEO & Co-Founder','https://triaxistechnologies.com/','exa',NULL,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(16,9,'Ebenezer Antwi-Badu','West Africa Regional Head, TriAxis Technologies','https://triaxistechnologies.com/','exa',NULL,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(17,12,'Huw Foley','Chief Technology Officer','https://www.linkedin.com/in/huw-foley-761ba183','exa',NULL,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(18,12,'Sataphat Suphasoet','Head of Engineering','https://linkedin.com/in/sataphat-suphasoet','exa',NULL,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(19,12,'Phil Goffin','Founder & CEO','https://www.zilo.co.uk/team/phil-goffin','exa',NULL,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(20,14,'Lantam Dennis','CTO & Product Manager','http://www.wantechsolutions.com/lantam.html','exa',NULL,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(21,14,'Sulemana Akati Braimah','CEO & COO','http://www.wantechsolutions.com/','exa',NULL,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(22,14,'Isaac T','Director, Software Dev.','http://www.wantechsolutions.com/','exa',NULL,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(23,15,'Olayiwola Allen','Chief Technology Officer','https://esolutionsghana.com/olayiwola-allen/','exa',93,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(24,15,'Victor Obeng-Adiyiah','Chief Executive Officer','https://esolutionsghana.com/our-people/','exa',NULL,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(25,15,'Gabriel Dela (Gabriel Mensah)','Chief Operating Officer','https://esolutionsghana.com/gabriel-dela/','exa',NULL,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(26,19,'Mawuli Denteh','Founder & CEO','https://linkedin.com/in/mawulidenteh','exa',98,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(27,28,'Kyere Emmanuel','CEO & Founder','https://emmaktech.com/about','exa',NULL,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(28,45,'Emeka K.','Head of Engineering','https://selescribe.com/about','exa',NULL,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(29,45,'Amb. John Sele Philip','Founder & CEO of Sele Media Africa','https://selescribe.com/sele-media','exa',NULL,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(30,46,'Peter Alfred-Adekeye','Founder & CEO','https://photonai.ai/about/press.html','exa',NULL,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(31,55,'Ayodeji Niyi-Adesola','Chief Executive Officer (CEO), HostNowNow','https://x-ray.contact/identities/ayodeji-niyi-adesola-email-and-phone/63fc0a37c45ae4c13f62036f/','exa',108,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(32,63,'Patrick Simpe-Asante','Co-founder and Director of Software Engineering','https://orgmento.com/team/patrick/','exa',113,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(33,63,'Phyllis Boakye Simpe-Asante','Co-Founder and Director','https://linkedin.com/in/phyllis-boakye','exa',114,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(34,64,'Louis Amenyo Adanuty','Founder and CEO','https://linkedin.com/in/louis-amenyo-adanuty-42609b31','exa',NULL,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(35,64,'Shallom Teksol','HR','https://linkedin.com/in/shallom-teksol-50aa7668','exa',NULL,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(36,66,'John Anwoh','CEO and CTO','https://excedi.com/','exa',NULL,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(37,66,'Paul Acquah','Head of Ops','https://excedi.com/','exa',NULL,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(38,66,'Gasu Daniel','Backend Specialist','https://excedi.com/','exa',NULL,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(39,68,'BRIGHT WIREDU NUAKOH','Co-Founder & AI Expert','https://linkedin.com/company/medirevs','exa',NULL,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(40,68,'Dorothy Sagoe','Co-founder and Data Scientist','https://linkedin.com/company/medirevs','exa',NULL,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(41,68,'Winner Ahadzivia','Co-Founder and AI Lead','https://linkedin.com/company/medirevs','exa',NULL,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(42,72,'Senyo Mawuli Jiagge','Co-founder & CEO','https://linkedin.com/in/senyo-mawuli-jiagge-b28312115','exa',NULL,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(43,72,'Dr. Basil Sefordzi-Amuzu','CIO','https://dealsourceafrica.co/companies/qknow-avenir-company-limited/','exa',NULL,'2026-10-11 05:32:27');
INSERT INTO "people" VALUES(44,74,'Precious Asiegbu','Chief Technology Officer','https://linkedin.com/company/edfrica','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(45,77,'Enoch Oppong Agyei','Founder & CEO','https://linkedin.com/in/promzytechsolutions','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(46,79,'Joseph Ekpaha-Kwofie','Founder and CEO','https://www.f6s.com/member/joseph-ekpaha-kwofie','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(47,79,'Enock Aboagye Assiamah','Co-Founder, UI/UX Designer','https://www.f6s.com/company/tuduafrica','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(48,81,'Rodger Adjadi','Company manager / Developer','https://www.ghanayello.com/company/49931/Shopbeta_Online_Mall','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(49,82,'Mamudu Kamilo','Founder & CEO','https://linkedin.com/in/mamudu-kamilo-853b03178','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(50,86,'Daniel Lamptey','Technical Director','https://linkedin.com/in/daniel-lamptey-9402325','exa',127,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(51,86,'Emmanuel Sekyere Asiedu','President & Founder / CEO','https://www.virtualinfosecafrica.com/team','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(52,86,'Jim Harris T.','Risk and Compliance Lead','https://linkedin.com/company/via-ghana','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(53,87,'Callum Kottis','Senior Vice President, Technical Delivery','https://thecyberhawk.com/the-team','exa',128,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(54,87,'Chris Fleming','Chief Executive Officer','https://thecyberhawk.com/the-team','exa',129,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(55,87,'Phil Buchan','Chief Operating Officer','https://thecyberhawk.com/the-team','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(56,87,'Nick Stewart','Chief Information Officer','https://linkedin.com/in/nickstewart','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(57,87,'David Storey','Manager, Software Engineering','https://thecyberhawk.com/the-team','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(58,87,'Robert Seggelke','Vice President, People Operation','https://thecyberhawk.com/the-team','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(59,90,'Gervin Appiah','CEO, Founder, Principal Hacking Officer, Lead Operator','https://oosecgh.com/about/','exa',133,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(60,91,'Samuel K. Boateng','Founder & CEO','https://linkedin.com/in/doctor-it','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(61,91,'Francisca Boateng','Co-Founder & Director of Operations','https://linkedin.com/company/slammllc','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(62,91,'Kelvin Nuamah','Software Engineer - Django Specialist','https://aeroleads.com/c/slammghana','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(63,92,'Kwabena Asante-Acheampong','Security Assessment Director','https://kronixshield.com/','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(64,92,'Adwoa Mensah-Bonsu','GRC & Compliance Lead','https://kronixshield.com/','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(65,92,'Kofi Boateng','Infrastructure Hardening Lead','https://kronixshield.com/','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(66,92,'Ama Osei-Frimpong','Monitoring & Detection Manager','https://kronixshield.com/','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(67,92,'Yaw Darko','Vulnerability Management Lead','https://kronixshield.com/','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(68,92,'Efua Agyeman-Duodu','Identity & Access Advisory Manager','https://kronixshield.com/','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(69,95,'Nutifafa Amedior','Business Intelligence Lead','https://linkedin.com/company/lunartribeltd','exa',138,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(70,96,'Victor Odame','Chief Technology Officer','https://linkedin.com/in/victor-odame-143ba9137','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(71,96,'Henry Kwamena Baffoe','Managing Director and Co-founder','https://linkedin.com/in/henry-kwamena-baffoe-b35324100','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(72,97,'Albert Sanjay Dansoh','CTO','https://linkedin.com/company/beron-intelligence','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(73,99,'Osei Kofi Tweneboah, Ph.D.','Founder and CEO, Principal Data Scientist','https://www.mogitalanalytics.com/team','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(74,100,'Jai Bhatia','Co-Founder and CTO','https://linkedin.com/in/bhatia-jai','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(75,100,'Jaap Gielink','Co-founder & CEO','https://linkedin.com/company/datamonkai','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(76,100,'Rahul Gupta','Founder and CEO','https://linkedin.com/in/rahul1990gupta','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(77,100,'Matthew Condron','Chief Delivery & Solutions Officer','https://linkedin.com/company/datamonkai','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(78,100,'John in ''t Hout','Founding Engineer','https://www.linkedin.com/posts/bhatia-jai_datamonkai-is-out-of-stealth-and-were-activity-7246776437955784705-l6jV','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(79,102,'Nayram Mensah','Chief Technology Officer','https://techlabari.com/myfig-wins-at-innolab-insuretech-accelerator-programme-in-ghana/','exa',145,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(80,102,'Festus William Amoyaw','Co-Founder & CEO','https://linkedin.com/company/figtech-llc','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(81,102,'Benjamin Kwashie','Full Stack Engineer','https://linkedin.com/in/benjaminkwashie','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(82,103,'David Igiebor','Co-Founder and CTO','https://www.linkedin.com/posts/david-igiebor_startup-cofounder-entrepreneurship-activity-7415844219803725824-ORTm','exa',146,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(83,104,'Zangui Nimondo','Chief Technology Officer','https://www.ridewithmaya.com/maya-team-profiles','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(84,104,'Alfred Kissiedu Ludwig','Co-Founder','https://www.ridewithmaya.com/maya-team-profiles','exa',147,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(85,104,'Lois Adwoa Adusei','Co-Founder','https://www.ridewithmaya.com/maya-team-profiles','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(86,105,'Edwin Nyawoli','CTO','https://wonfliki.com/about-us/','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(87,105,'Hillary W. Adare','Founder','https://wonfliki.com/about-us/','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(88,108,'Emmanuel Essel Acheampong','Founder & CEO','https://www.agrisattechnologies.com/about','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(89,109,'Peter O''Hara Adu','Chief Technology Officer','https://linkedin.com/in/peter-ohara-adu','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(90,109,'Isaac Sesi','Founder and CEO, Head Of Product Development','https://linkedin.com/in/isaacsesi','exa',152,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(91,109,'Ayatullahi Zakaria','Head of Hardware','https://sesitechnologies.com/sesi-technologies-academy/','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(92,109,'Papa Kwaku Afful','Head of Mechanical engineering','https://sesitechnologies.com/sesi-technologies-academy/','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(93,112,'Selassie Sallas-Mensah','Founder & CEO, Lead AI SaaS Engineer / Product Owner','https://linkedin.com/in/selassiesallas','exa',NULL,'2026-10-11 05:32:28');
INSERT INTO "people" VALUES(94,113,'Leonard','Founder, Full stack developer + CTO','https://modularpath.dev/about','exa',NULL,'2026-10-11 05:32:29');
INSERT INTO "people" VALUES(95,113,'Boateng','Co-Founder, Cyber Security Lead + Engineering','https://modularpath.dev/about','exa',NULL,'2026-10-11 05:32:29');
INSERT INTO "people" VALUES(96,117,'Abeyie Bonsu Schmutz','Co-Founder','https://linkedin.com/in/abeyie-bonsu-schmutz','exa',158,'2026-10-11 05:32:29');
INSERT INTO "people" VALUES(97,117,'Joy Bonsu Schmutz','Co-Founder','https://linkedin.com/company/abeyie-digital-business-services','exa',159,'2026-10-11 05:32:29');
INSERT INTO "people" VALUES(98,119,'Zeeshan Khalid','Chief Technology Officer','https://www.4th-ir.com/about-us','exa',170,'2026-10-11 05:32:29');
INSERT INTO "people" VALUES(99,119,'Thomas Gustinis','Chief Executive Officer','https://www.4th-ir.com/about-us','exa',171,'2026-10-11 05:32:29');
INSERT INTO "people" VALUES(100,119,'Jonathan Kaufman','CPO and Head of AI','https://linkedin.com/company/4th-ir','exa',NULL,'2026-10-11 05:32:29');
INSERT INTO "people" VALUES(101,119,'Reid Anderson','Head Resourcing Services','https://growjo.com/company/4th-IR','exa',NULL,'2026-10-11 05:32:29');
INSERT INTO "people" VALUES(102,6,'Frank Abudey',NULL,NULL,'prospeo',NULL,'2026-10-11 05:36:27');
INSERT INTO "people" VALUES(103,35,'Sylvester Horsu',NULL,NULL,'prospeo',NULL,'2026-10-11 05:36:27');
INSERT INTO "people" VALUES(104,35,'Pierrette Ahiadorme',NULL,NULL,'prospeo',NULL,'2026-10-11 05:36:27');
INSERT INTO "people" VALUES(105,35,'Ronald Osei',NULL,NULL,'prospeo',NULL,'2026-10-11 05:36:27');
INSERT INTO "people" VALUES(106,35,'Patience Amoako-Adams',NULL,NULL,'prospeo',NULL,'2026-10-11 05:36:27');
INSERT INTO "people" VALUES(107,64,'Francis Yao Agbolosoo',NULL,NULL,'prospeo',NULL,'2026-10-11 05:36:27');
INSERT INTO "people" VALUES(108,34,'Jackson Janey','Founder','https://telenet.com.gh/team/our-team/','exa',NULL,'2026-10-11 05:39:28');
INSERT INTO "people" VALUES(109,34,'Lesia Travis','Co-Founder','https://telenet.com.gh/team/our-team/','exa',NULL,'2026-10-11 05:39:28');
INSERT INTO "people" VALUES(110,123,'Nii Tetteh','Chief Technology Officer (Current) / Partner at expressPay Ghana Limited','https://linkedin.com/in/nii-tetteh-17930130a','exa',194,'2026-10-15 07:04:02');
INSERT INTO "people" VALUES(111,123,'Curtis Vanderpuije','Co-Founder and CEO',NULL,'exa',195,'2026-10-15 07:04:02');
INSERT INTO "people" VALUES(112,127,'Molly Mackinlay','Head of Engineering, Product, & Research Development','https://theorg.com/org/protocol-labs/teams/engineering-and-development','exa',208,'2026-10-15 07:05:01');
INSERT INTO "people" VALUES(113,127,'Mykhailo Bondarchuk','Head of Engineering','https://linkedin.com/in/mykhailo-bondarchuk-6a0619335','exa',NULL,'2026-10-15 07:05:01');
INSERT INTO "people" VALUES(114,127,'Estefania Henao','Head of People','https://theorg.com/org/protocol-labs','exa',NULL,'2026-10-15 07:05:01');
INSERT INTO "people" VALUES(115,127,'Juan Benet','Founder and CEO','https://www.ycombinator.com/companies/protocol-labs','exa',NULL,'2026-10-15 07:05:01');
INSERT INTO "people" VALUES(116,126,'Matt Machuga','VP Engineering','https://linkedin.com/in/machuga','exa',219,'2026-10-15 07:05:20');
INSERT INTO "people" VALUES(117,126,'Jakub Kratina','Director of Engineering','https://linkedin.com/in/jakub-kratina-b5972549','exa',220,'2026-10-15 07:05:20');
INSERT INTO "people" VALUES(118,121,'Shahnavaz Syed','Founder','https://www.huraintechnologies.com/about','exa',NULL,'2026-10-15 07:05:53');
INSERT INTO "people" VALUES(119,121,'Dinesh Prajapati','Leads the Hurain Technologies development team','https://www.huraintechnologies.com/about','exa',NULL,'2026-10-15 07:05:53');
INSERT INTO "people" VALUES(120,131,'Muhammad Adnan Tariq','Chief Technology Officer','https://linkedin.com/in/madnantariq','exa',262,'2026-10-15 07:45:11');
INSERT INTO "people" VALUES(121,131,'Ilan Rakhmanov','Founder & CEO','https://linkedin.com/in/ceoguy','exa',261,'2026-10-15 07:45:11');
CREATE INDEX idx_companies_domain ON companies(domain);
CREATE UNIQUE INDEX idx_contacts_primary
    ON contacts(company_id)
    WHERE is_primary = 1;
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('companies',137);
INSERT INTO "sqlite_sequence" VALUES('contacts',265);
INSERT INTO "sqlite_sequence" VALUES('outreaches',73);
INSERT INTO "sqlite_sequence" VALUES('inbox_events',11);
INSERT INTO "sqlite_sequence" VALUES('people',121);
COMMIT;
