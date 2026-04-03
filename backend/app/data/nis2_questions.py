"""
kOne NIS2 Compliance Assessment — Question Database
Based on Czech Cybersecurity Act (Act No. 264/2025 Coll.) implementing EU NIS2 Directive.

Each domain maps to a requirement area from the Act.
Each question has:
  - id: unique identifier
  - text_cs: Czech language question
  - text_en: English translation
  - weight: how heavily this impacts the compliance score (1-5)
  - remediation_hint: what to do if the answer is "no"
  - article_ref: reference to the relevant NIS2 article or Czech Act section
"""

NIS2_DOMAINS = [
    {
        "id": "governance",
        "name_cs": "Řízení kybernetické bezpečnosti",
        "name_en": "Cybersecurity governance",
        "description_cs": "Odpovědnost vedení a organizační struktura kybernetické bezpečnosti",
        "description_en": "Management accountability and organizational structure for cybersecurity",
        "article_ref": "NIS2 Art. 20",
        "questions": [
            {
                "id": "gov_01",
                "text_cs": "Má vaše organizace jmenovanou osobu odpovědnou za kybernetickou bezpečnost?",
                "text_en": "Does your organization have a designated person responsible for cybersecurity?",
                "weight": 5,
                "remediation_hint": "Appoint a cybersecurity officer or assign clear cybersecurity responsibility to a senior manager. This person must report directly to the executive board.",
                "article_ref": "NIS2 Art. 20(1)"
            },
            {
                "id": "gov_02",
                "text_cs": "Prošlo vedení organizace školením v oblasti kybernetické bezpečnosti?",
                "text_en": "Has the organization's management undergone cybersecurity training?",
                "weight": 4,
                "remediation_hint": "Schedule mandatory cybersecurity awareness training for all board members and senior executives. NIS2 requires management to have sufficient knowledge to assess cyber risks.",
                "article_ref": "NIS2 Art. 20(2)"
            },
            {
                "id": "gov_03",
                "text_cs": "Existuje schválená bezpečnostní politika (ISMS) pro celou organizaci?",
                "text_en": "Is there an approved security policy (ISMS) covering the entire organization?",
                "weight": 5,
                "remediation_hint": "Develop and formally approve a comprehensive information security management policy. Consider aligning with ISO 27001 framework as a baseline.",
                "article_ref": "NIS2 Art. 21(2)(a)"
            },
            {
                "id": "gov_04",
                "text_cs": "Je bezpečnostní politika pravidelně revidována (minimálně jednou ročně)?",
                "text_en": "Is the security policy reviewed regularly (at least annually)?",
                "weight": 3,
                "remediation_hint": "Establish an annual review cycle for all security policies. Document each review with date, changes made, and approval signatures.",
                "article_ref": "NIS2 Art. 21(2)(a)"
            },
            {
                "id": "gov_05",
                "text_cs": "Má vaše organizace dokumentovaný plán řízení rizik?",
                "text_en": "Does your organization have a documented risk management plan?",
                "weight": 5,
                "remediation_hint": "Create a risk treatment plan that identifies assets, threats, vulnerabilities, and the measures to mitigate each risk. This is a core requirement under the Czech Cybersecurity Act.",
                "article_ref": "NIS2 Art. 21(1)"
            },
        ]
    },
    {
        "id": "incident_response",
        "name_cs": "Řízení incidentů",
        "name_en": "Incident response",
        "description_cs": "Schopnost detekce, hlášení a reakce na kybernetické incidenty",
        "description_en": "Capability to detect, report, and respond to cybersecurity incidents",
        "article_ref": "NIS2 Art. 23",
        "questions": [
            {
                "id": "ir_01",
                "text_cs": "Má vaše organizace zdokumentovaný plán reakce na incidenty?",
                "text_en": "Does your organization have a documented incident response plan?",
                "weight": 5,
                "remediation_hint": "Develop an incident response plan covering detection, containment, eradication, recovery, and lessons learned. Include contact details for NÚKIB and your CSIRT.",
                "article_ref": "NIS2 Art. 21(2)(b)"
            },
            {
                "id": "ir_02",
                "text_cs": "Víte, že musíte nahlásit významný incident NÚKIB do 24 hodin?",
                "text_en": "Are you aware that significant incidents must be reported to NÚKIB within 24 hours?",
                "weight": 5,
                "remediation_hint": "Establish a reporting procedure: early warning to NÚKIB within 24 hours, incident report within 72 hours, and final report within 1 month. Train your team on these deadlines.",
                "article_ref": "NIS2 Art. 23(4)"
            },
            {
                "id": "ir_03",
                "text_cs": "Provádíte pravidelná cvičení reakce na incidenty (alespoň jednou ročně)?",
                "text_en": "Do you conduct regular incident response drills (at least annually)?",
                "weight": 3,
                "remediation_hint": "Schedule at least one tabletop exercise per year simulating a cyberattack. Document the exercise, findings, and improvements made.",
                "article_ref": "NIS2 Art. 21(2)(b)"
            },
            {
                "id": "ir_04",
                "text_cs": "Máte zavedený systém pro detekci bezpečnostních událostí (SIEM, IDS/IPS)?",
                "text_en": "Do you have a system for detecting security events (SIEM, IDS/IPS)?",
                "weight": 4,
                "remediation_hint": "Implement at minimum a log collection and monitoring solution. Open-source options like Wazuh or ELK Stack can serve as a starting point for smaller organizations.",
                "article_ref": "NIS2 Art. 21(2)(b)"
            },
            {
                "id": "ir_05",
                "text_cs": "Máte definované role a odpovědnosti pro řízení incidentů?",
                "text_en": "Do you have defined roles and responsibilities for incident management?",
                "weight": 4,
                "remediation_hint": "Create an incident response team with clearly assigned roles: incident coordinator, technical analyst, communications lead, and management liaison.",
                "article_ref": "NIS2 Art. 21(2)(b)"
            },
        ]
    },
    {
        "id": "business_continuity",
        "name_cs": "Kontinuita činností",
        "name_en": "Business continuity",
        "description_cs": "Zajištění kontinuity provozu a obnova po havárii",
        "description_en": "Ensuring operational continuity and disaster recovery",
        "article_ref": "NIS2 Art. 21(2)(c)",
        "questions": [
            {
                "id": "bc_01",
                "text_cs": "Má vaše organizace plán kontinuity podnikání (BCP)?",
                "text_en": "Does your organization have a business continuity plan (BCP)?",
                "weight": 5,
                "remediation_hint": "Develop a BCP that identifies critical business processes, maximum tolerable downtime for each, and the steps to maintain operations during a disruption.",
                "article_ref": "NIS2 Art. 21(2)(c)"
            },
            {
                "id": "bc_02",
                "text_cs": "Provádíte pravidelné zálohování kritických dat?",
                "text_en": "Do you perform regular backups of critical data?",
                "weight": 5,
                "remediation_hint": "Implement automated backups following the 3-2-1 rule: 3 copies, 2 different media types, 1 offsite. Test restore procedures quarterly.",
                "article_ref": "NIS2 Art. 21(2)(c)"
            },
            {
                "id": "bc_03",
                "text_cs": "Testujete pravidelně obnovu ze zálohy?",
                "text_en": "Do you regularly test restoration from backups?",
                "weight": 4,
                "remediation_hint": "Schedule quarterly backup restoration tests. Document the test results including time to restore and data integrity verification.",
                "article_ref": "NIS2 Art. 21(2)(c)"
            },
            {
                "id": "bc_04",
                "text_cs": "Máte plán obnovy po havárii (DRP) pro vaše kritické systémy?",
                "text_en": "Do you have a disaster recovery plan (DRP) for your critical systems?",
                "weight": 5,
                "remediation_hint": "Create a DRP specifying recovery time objectives (RTO) and recovery point objectives (RPO) for each critical system. Include failover procedures and responsible personnel.",
                "article_ref": "NIS2 Art. 21(2)(c)"
            },
        ]
    },
    {
        "id": "supply_chain",
        "name_cs": "Bezpečnost dodavatelského řetězce",
        "name_en": "Supply chain security",
        "description_cs": "Řízení bezpečnostních rizik spojených s dodavateli a třetími stranami",
        "description_en": "Managing security risks from suppliers and third parties",
        "article_ref": "NIS2 Art. 21(2)(d)",
        "questions": [
            {
                "id": "sc_01",
                "text_cs": "Máte přehled o všech kritických dodavatelích IT služeb a produktů?",
                "text_en": "Do you maintain an inventory of all critical IT service and product suppliers?",
                "weight": 4,
                "remediation_hint": "Create and maintain a register of all IT suppliers including what services/products they provide, data they access, and their criticality to your operations.",
                "article_ref": "NIS2 Art. 21(2)(d)"
            },
            {
                "id": "sc_02",
                "text_cs": "Zahrnují vaše smlouvy s dodavateli bezpečnostní požadavky?",
                "text_en": "Do your supplier contracts include cybersecurity requirements?",
                "weight": 4,
                "remediation_hint": "Update supplier contracts to include security clauses: data protection obligations, incident notification requirements, right to audit, and compliance with relevant standards.",
                "article_ref": "NIS2 Art. 21(2)(d)"
            },
            {
                "id": "sc_03",
                "text_cs": "Provádíte hodnocení bezpečnostních rizik u vašich dodavatelů?",
                "text_en": "Do you assess cybersecurity risks of your suppliers?",
                "weight": 4,
                "remediation_hint": "Implement a supplier risk assessment process. At minimum, send security questionnaires to critical suppliers and review their certifications (ISO 27001, SOC 2).",
                "article_ref": "NIS2 Art. 21(2)(d)"
            },
            {
                "id": "sc_04",
                "text_cs": "Máte proces pro řízení přístupu dodavatelů k vašim systémům?",
                "text_en": "Do you have a process for managing supplier access to your systems?",
                "weight": 4,
                "remediation_hint": "Implement strict access controls for third-party vendors: dedicated accounts, least-privilege access, activity logging, and regular access reviews.",
                "article_ref": "NIS2 Art. 21(2)(d)"
            },
        ]
    },
    {
        "id": "access_control",
        "name_cs": "Řízení přístupu",
        "name_en": "Access control",
        "description_cs": "Správa přístupů, autentizace a oprávnění",
        "description_en": "Management of access, authentication, and authorization",
        "article_ref": "NIS2 Art. 21(2)(i)",
        "questions": [
            {
                "id": "ac_01",
                "text_cs": "Používáte vícefaktorovou autentizaci (MFA) pro přístup ke kritickým systémům?",
                "text_en": "Do you use multi-factor authentication (MFA) for access to critical systems?",
                "weight": 5,
                "remediation_hint": "Deploy MFA on all critical systems, admin accounts, VPN access, and email. Start with TOTP-based authenticator apps as a minimum.",
                "article_ref": "NIS2 Art. 21(2)(j)"
            },
            {
                "id": "ac_02",
                "text_cs": "Máte zavedenu politiku silných hesel?",
                "text_en": "Do you have a strong password policy in place?",
                "weight": 3,
                "remediation_hint": "Enforce minimum 12-character passwords, prohibit common passwords, and implement a password manager for the organization. Consider moving toward passwordless authentication.",
                "article_ref": "NIS2 Art. 21(2)(j)"
            },
            {
                "id": "ac_03",
                "text_cs": "Uplatňujete princip nejmenších oprávnění (least privilege)?",
                "text_en": "Do you apply the principle of least privilege?",
                "weight": 4,
                "remediation_hint": "Review all user accounts and permissions. Remove admin rights from users who don't need them. Implement role-based access control (RBAC).",
                "article_ref": "NIS2 Art. 21(2)(i)"
            },
            {
                "id": "ac_04",
                "text_cs": "Provádíte pravidelnou revizi přístupových oprávnění?",
                "text_en": "Do you conduct regular access rights reviews?",
                "weight": 3,
                "remediation_hint": "Schedule quarterly reviews of all user access rights. Immediately revoke access for departing employees. Document all reviews.",
                "article_ref": "NIS2 Art. 21(2)(i)"
            },
            {
                "id": "ac_05",
                "text_cs": "Máte zavedený proces pro správu privilegovaných účtů?",
                "text_en": "Do you have a process for managing privileged accounts?",
                "weight": 4,
                "remediation_hint": "Implement privileged access management: separate admin accounts from daily-use accounts, log all privileged actions, and require MFA for all admin access.",
                "article_ref": "NIS2 Art. 21(2)(i)"
            },
        ]
    },
    {
        "id": "encryption",
        "name_cs": "Šifrování a kryptografie",
        "name_en": "Encryption and cryptography",
        "description_cs": "Použití šifrování pro ochranu dat při přenosu a uložení",
        "description_en": "Use of encryption to protect data in transit and at rest",
        "article_ref": "NIS2 Art. 21(2)(h)",
        "questions": [
            {
                "id": "enc_01",
                "text_cs": "Šifrujete data při přenosu (TLS/HTTPS)?",
                "text_en": "Do you encrypt data in transit (TLS/HTTPS)?",
                "weight": 4,
                "remediation_hint": "Ensure all web services use HTTPS with TLS 1.2 or higher. Redirect all HTTP traffic to HTTPS. Use tools like SSL Labs to verify your configuration.",
                "article_ref": "NIS2 Art. 21(2)(h)"
            },
            {
                "id": "enc_02",
                "text_cs": "Šifrujete citlivá data v úložišti (at rest)?",
                "text_en": "Do you encrypt sensitive data at rest?",
                "weight": 4,
                "remediation_hint": "Enable encryption on all storage containing sensitive data: full disk encryption on endpoints (BitLocker, FileVault), database encryption, and encrypted backups.",
                "article_ref": "NIS2 Art. 21(2)(h)"
            },
            {
                "id": "enc_03",
                "text_cs": "Máte politiku pro správu kryptografických klíčů?",
                "text_en": "Do you have a cryptographic key management policy?",
                "weight": 3,
                "remediation_hint": "Document how encryption keys are generated, stored, rotated, and revoked. Keys should never be stored alongside the data they protect.",
                "article_ref": "NIS2 Art. 21(2)(h)"
            },
        ]
    },
    {
        "id": "vulnerability_mgmt",
        "name_cs": "Řízení zranitelností",
        "name_en": "Vulnerability management",
        "description_cs": "Odhalování, hodnocení a odstraňování zranitelností",
        "description_en": "Discovery, assessment, and remediation of vulnerabilities",
        "article_ref": "NIS2 Art. 21(2)(e)",
        "questions": [
            {
                "id": "vm_01",
                "text_cs": "Provádíte pravidelné skenování zranitelností?",
                "text_en": "Do you perform regular vulnerability scanning?",
                "weight": 4,
                "remediation_hint": "Implement automated vulnerability scanning at least monthly. Open-source tools like OpenVAS or Greenbone can be used as a starting point.",
                "article_ref": "NIS2 Art. 21(2)(e)"
            },
            {
                "id": "vm_02",
                "text_cs": "Máte proces pro včasné nasazování bezpečnostních záplat?",
                "text_en": "Do you have a process for timely deployment of security patches?",
                "weight": 5,
                "remediation_hint": "Establish a patching policy: critical patches within 48 hours, high within 1 week, medium within 1 month. Use automated patch management tools where possible.",
                "article_ref": "NIS2 Art. 21(2)(e)"
            },
            {
                "id": "vm_03",
                "text_cs": "Máte přehled o všech IT aktivech (hardware, software, síťové prvky)?",
                "text_en": "Do you maintain an inventory of all IT assets (hardware, software, network devices)?",
                "weight": 4,
                "remediation_hint": "Create and maintain a comprehensive asset inventory. You cannot protect what you don't know exists. Update it whenever assets are added, changed, or removed.",
                "article_ref": "NIS2 Art. 21(2)(e)"
            },
            {
                "id": "vm_04",
                "text_cs": "Provádíte penetrační testování (alespoň jednou ročně)?",
                "text_en": "Do you perform penetration testing (at least annually)?",
                "weight": 3,
                "remediation_hint": "Engage a qualified penetration testing provider at least annually. For essential entities under the Czech Act, this is strongly recommended. Document and remediate findings.",
                "article_ref": "NIS2 Art. 21(2)(e)"
            },
        ]
    },
    {
        "id": "network_security",
        "name_cs": "Bezpečnost sítí a informačních systémů",
        "name_en": "Network and information system security",
        "description_cs": "Zabezpečení sítí, segmentace a monitoring",
        "description_en": "Network security, segmentation, and monitoring",
        "article_ref": "NIS2 Art. 21(2)(e)",
        "questions": [
            {
                "id": "ns_01",
                "text_cs": "Používáte firewall pro ochranu vaší sítě?",
                "text_en": "Do you use a firewall to protect your network?",
                "weight": 5,
                "remediation_hint": "Deploy and properly configure firewalls at network boundaries. Review firewall rules regularly and remove unnecessary open ports.",
                "article_ref": "NIS2 Art. 21(2)(e)"
            },
            {
                "id": "ns_02",
                "text_cs": "Je vaše síť segmentována (oddělení kritických systémů)?",
                "text_en": "Is your network segmented (separation of critical systems)?",
                "weight": 4,
                "remediation_hint": "Implement network segmentation using VLANs or separate subnets. At minimum, separate: production systems, development, guest Wi-Fi, and management networks.",
                "article_ref": "NIS2 Art. 21(2)(e)"
            },
            {
                "id": "ns_03",
                "text_cs": "Monitorujete síťový provoz pro detekci anomálií?",
                "text_en": "Do you monitor network traffic for anomaly detection?",
                "weight": 3,
                "remediation_hint": "Implement network monitoring to detect unusual traffic patterns. Solutions range from simple NetFlow analysis to full network detection and response (NDR) tools.",
                "article_ref": "NIS2 Art. 21(2)(e)"
            },
            {
                "id": "ns_04",
                "text_cs": "Používáte zabezpečené připojení pro vzdálený přístup (VPN)?",
                "text_en": "Do you use secure connections for remote access (VPN)?",
                "weight": 4,
                "remediation_hint": "Require VPN or zero-trust network access for all remote connections. Ensure the VPN uses strong encryption and requires MFA.",
                "article_ref": "NIS2 Art. 21(2)(e)"
            },
        ]
    },
    {
        "id": "cyber_hygiene",
        "name_cs": "Kybernetická hygiena a školení",
        "name_en": "Cyber hygiene and training",
        "description_cs": "Školení zaměstnanců a základní bezpečnostní praktiky",
        "description_en": "Employee training and basic security practices",
        "article_ref": "NIS2 Art. 21(2)(g)",
        "questions": [
            {
                "id": "ch_01",
                "text_cs": "Provádíte pravidelná školení kybernetické bezpečnosti pro všechny zaměstnance?",
                "text_en": "Do you conduct regular cybersecurity training for all employees?",
                "weight": 4,
                "remediation_hint": "Implement mandatory annual cybersecurity awareness training for all employees. Cover phishing recognition, password hygiene, social engineering, and incident reporting.",
                "article_ref": "NIS2 Art. 21(2)(g)"
            },
            {
                "id": "ch_02",
                "text_cs": "Provádíte simulace phishingových útoků?",
                "text_en": "Do you conduct phishing simulation exercises?",
                "weight": 3,
                "remediation_hint": "Run quarterly phishing simulations to test employee awareness. Track click rates over time and provide additional training for employees who fail.",
                "article_ref": "NIS2 Art. 21(2)(g)"
            },
            {
                "id": "ch_03",
                "text_cs": "Máte bezpečnostní politiku pro používání vlastních zařízení (BYOD)?",
                "text_en": "Do you have a security policy for bring-your-own-device (BYOD)?",
                "weight": 3,
                "remediation_hint": "Create a BYOD policy covering minimum security requirements for personal devices: encryption, screen lock, OS updates, and remote wipe capability.",
                "article_ref": "NIS2 Art. 21(2)(g)"
            },
            {
                "id": "ch_04",
                "text_cs": "Mají zaměstnanci jasné pokyny, jak hlásit podezřelé aktivity?",
                "text_en": "Do employees have clear instructions on how to report suspicious activities?",
                "weight": 4,
                "remediation_hint": "Establish a simple, well-publicized reporting channel (email, internal tool, phone number) for employees to report suspicious emails, activities, or security concerns.",
                "article_ref": "NIS2 Art. 21(2)(g)"
            },
        ]
    },
    {
        "id": "asset_classification",
        "name_cs": "Klasifikace aktiv a dat",
        "name_en": "Asset and data classification",
        "description_cs": "Klasifikace informačních systémů a dat podle bezpečnostních úrovní",
        "description_en": "Classification of information systems and data by security levels",
        "article_ref": "Czech Cybersecurity Act §8",
        "questions": [
            {
                "id": "asc_01",
                "text_cs": "Máte klasifikaci svých informačních systémů podle bezpečnostních úrovní (základní, významné, vysoké)?",
                "text_en": "Have you classified your information systems by security levels (basic, significant, high)?",
                "weight": 5,
                "remediation_hint": "The Czech Cybersecurity Act requires entities to classify their electronic information systems into three security levels: basic, significant, or high. This classification is based on risks to data integrity, system availability, and data confidentiality.",
                "article_ref": "Czech Cybersecurity Act §8"
            },
            {
                "id": "asc_02",
                "text_cs": "Máte klasifikaci dat podle stupně citlivosti?",
                "text_en": "Do you classify data according to sensitivity levels?",
                "weight": 4,
                "remediation_hint": "Implement a data classification scheme (e.g., Public, Internal, Confidential, Restricted). Apply appropriate security controls based on classification level.",
                "article_ref": "Czech Cybersecurity Act §8"
            },
            {
                "id": "asc_03",
                "text_cs": "Jsou bezpečnostní opatření přizpůsobena klasifikaci vašich systémů?",
                "text_en": "Are security measures tailored to the classification of your systems?",
                "weight": 4,
                "remediation_hint": "Map your security controls to each system classification level. Higher-classified systems require stricter measures for access control, monitoring, and encryption.",
                "article_ref": "Czech Cybersecurity Act §8"
            },
        ]
    },
]


def get_all_questions():
    """Return a flat list of all questions with their domain info."""
    questions = []
    for domain in NIS2_DOMAINS:
        for q in domain["questions"]:
            questions.append({
                **q,
                "domain_id": domain["id"],
                "domain_name_cs": domain["name_cs"],
                "domain_name_en": domain["name_en"],
            })
    return questions


def get_total_max_score():
    """Calculate the maximum possible compliance score."""
    total = 0
    for domain in NIS2_DOMAINS:
        for q in domain["questions"]:
            total += q["weight"]
    return total


def get_domain_max_score(domain_id: str):
    """Calculate max score for a specific domain."""
    for domain in NIS2_DOMAINS:
        if domain["id"] == domain_id:
            return sum(q["weight"] for q in domain["questions"])
    return 0
