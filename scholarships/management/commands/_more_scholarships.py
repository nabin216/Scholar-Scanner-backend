from datetime import date

# Second batch of well-known international scholarships, loaded by load_real_scholarships.
# Same shape as SCHOLARSHIPS in load_real_scholarships.py. Deadlines are the expected next
# deadline; amount is an approximate yearly value in USD.


def s(title, provider, country, amount, open_date, deadline, url, levels, fields, fund, sponsors,
      categories, languages, featured, description):
    return {
        'title': title, 'provider': provider, 'country': country, 'amount': amount,
        'open_date': open_date, 'deadline': deadline, 'application_url': url, 'levels': levels,
        'fields': fields, 'fund_types': fund, 'sponsors': sponsors, 'categories': categories,
        'languages': languages, 'featured': featured, 'description': description,
    }


FULL = ['Full Funding']
PARTIAL = ['Partial Funding']
ANY = ['Any Field']
EN = ['IELTS', 'TOEFL']
GOV = ['Government']
UNI = ['University']
PRIV = ['Private Foundation']
MERIT = ['Merit-based']
STEM = ['Engineering', 'Computer Science', 'Natural Sciences']

MORE_SCHOLARSHIPS = [
    # ---------------- United Kingdom ----------------
    s('Marshall Scholarship', 'Marshall Aid Commemoration Commission', 'United Kingdom', 60000,
      date(2027, 5, 1), date(2027, 9, 28), 'https://www.marshallscholarship.org/',
      ['Master', 'PhD'], ANY, FULL, GOV, MERIT, [], True,
      '<p>Up to 50 scholarships a year for talented young Americans to study for a graduate degree '
      'at any UK university, funded by the British government.</p>'
      '<ul><li>University fees</li><li>Living and travel allowances</li><li>Fares to and from the US</li>'
      '<li>Thesis and research grants</li></ul>'
      '<p><strong>Eligibility:</strong> US citizens with a bachelor\'s degree and a GPA of at least 3.7. '
      'Applications are endorsed by your university and close in late September.</p>'),
    s('Clarendon Fund Scholarships', 'University of Oxford', 'United Kingdom', 55000,
      date(2026, 9, 1), date(2027, 1, 8), 'https://www.ox.ac.uk/clarendon',
      ['Master', 'PhD'], ANY, FULL, UNI, MERIT, EN, True,
      '<p>Oxford\'s flagship graduate scholarship scheme, offering around 140 new awards a year to '
      'academically excellent graduate applicants from all countries.</p>'
      '<ul><li>Full course fees</li><li>Generous annual living grant</li></ul>'
      '<p><strong>Eligibility:</strong> all graduate applicants are considered automatically when they apply '
      'for a degree-bearing course by the December or January deadline. No separate application is needed.</p>'),
    s('Commonwealth PhD Scholarships', 'Commonwealth Scholarship Commission in the UK', 'United Kingdom', 45000,
      date(2027, 8, 1), date(2027, 10, 12),
      'https://cscuk.fcdo.gov.uk/scholarships/commonwealth-phd-scholarships-least-developed-countries-and-fragile-states/',
      ['PhD'], ANY, FULL, GOV, ['Merit-based', 'Need-based'], ['IELTS'], False,
      '<p>Fully funded doctoral study at a UK university for talented candidates from least developed '
      'countries and fragile states in the Commonwealth.</p>'
      '<ul><li>Tuition fees</li><li>Return airfare</li><li>Monthly stipend</li>'
      '<li>Fieldwork and thesis grants</li></ul>'
      '<p><strong>Eligibility:</strong> citizen of an eligible Commonwealth country with a first-class or '
      'upper second-class degree (or a master\'s). Apply through your national nominating agency.</p>'),
    s('Commonwealth Shared Scholarships', 'Commonwealth Scholarship Commission and UK universities', 'United Kingdom',
      40000, date(2026, 9, 1), date(2026, 12, 16),
      'https://cscuk.fcdo.gov.uk/scholarships/commonwealth-shared-scholarships/',
      ['Master'], ANY, FULL, ['Government', 'University'], ['Need-based'], ['IELTS'], False,
      '<p>Jointly funded by the UK government and UK universities, these awards support one-year taught '
      'master\'s courses that contribute to development in low and middle income Commonwealth countries.</p>'
      '<ul><li>Tuition fees</li><li>Return airfare</li><li>Living stipend</li><li>Arrival allowance</li></ul>'
      '<p><strong>Eligibility:</strong> applicants who could not otherwise afford to study in the UK. '
      'Apply directly to a participating university.</p>'),
    s('GREAT Scholarships', 'British Council and UK universities', 'United Kingdom', 13000,
      date(2027, 1, 15), date(2027, 5, 31), 'https://study-uk.britishcouncil.org/scholarships-funding/great-scholarships',
      ['Master'], ANY, PARTIAL, ['Government', 'University'], MERIT, ['IELTS'], False,
      '<p>Scholarships worth at least GBP 10,000 towards tuition for a one-year postgraduate taught course '
      'at participating UK universities.</p>'
      '<ul><li>Minimum GBP 10,000 tuition award</li></ul>'
      '<p><strong>Eligibility:</strong> open to students from selected countries including Bangladesh, China, '
      'Egypt, Ghana, India, Indonesia, Kenya, Malaysia, Mexico, Nigeria, Pakistan, Thailand, Turkey and Vietnam. '
      'Each university sets its own deadline.</p>'),
    s("Imperial College President's PhD Scholarships", 'Imperial College London', 'United Kingdom', 45000,
      date(2026, 9, 1), date(2027, 1, 5), 'https://www.imperial.ac.uk/study/fees-and-funding/postgraduate-research/presidents-phd-scholarships/',
      ['PhD'], STEM + ['Business'], FULL, UNI, ['Research'], EN, False,
      '<p>Imperial\'s most prestigious PhD awards for exceptional research students in science, '
      'engineering, medicine and business.</p>'
      '<ul><li>Full tuition fees</li><li>Annual stipend of around GBP 25,000</li><li>Research consumables</li></ul>'
      '<p><strong>Eligibility:</strong> open to all nationalities. You need a supervisor at Imperial, who '
      'usually nominates you for the award.</p>'),
    s('Weidenfeld-Hoffmann Scholarships and Leadership Programme', 'Weidenfeld-Hoffmann Trust, University of Oxford',
      'United Kingdom', 55000, date(2026, 9, 1), date(2027, 1, 8), 'https://www.whtrust.org/',
      ['Master'], ANY, FULL, PRIV, MERIT, EN, False,
      '<p>Full scholarships for outstanding graduates from developing and emerging economies to study at '
      'Oxford, combined with a long-term leadership development programme.</p>'
      '<ul><li>Course fees</li><li>Living stipend</li><li>Leadership training and mentoring</li></ul>'
      '<p><strong>Eligibility:</strong> nationals of eligible countries who intend to return home to '
      'contribute to their country\'s development. Apply when applying to Oxford.</p>'),
    s('Skoll Scholarship', 'Saïd Business School, University of Oxford', 'United Kingdom', 90000,
      date(2026, 9, 1), date(2027, 1, 7), 'https://www.sbs.ox.ac.uk/programmes/degrees/mba/fees-and-funding/skoll-scholarship',
      ['Master'], ['Business'], FULL, ['University', 'Private Foundation'], MERIT, EN, False,
      '<p>Scholarships for social entrepreneurs to take the Oxford MBA followed by a master\'s or other '
      'degree, as part of the Skoll Centre community.</p>'
      '<ul><li>Full MBA course fees</li><li>Living stipend</li></ul>'
      '<p><strong>Eligibility:</strong> a track record of social impact and entrepreneurship. You must '
      'apply for the Oxford MBA by the stated scholarship round.</p>'),
    s('Pershing Square Graduate Scholarships', 'Saïd Business School, University of Oxford', 'United Kingdom', 90000,
      date(2026, 9, 1), date(2027, 1, 7), 'https://www.sbs.ox.ac.uk/programmes/degrees/mba/fees-and-funding/pershing-square-scholarship',
      ['Master'], ['Business'], FULL, ['University', 'Private Foundation'], MERIT, EN, False,
      '<p>Fully funded scholarships for a one-year master\'s followed by the one-year Oxford MBA '
      '(1+1), for future leaders who want to tackle world-scale problems.</p>'
      '<ul><li>Fees for both degrees</li><li>Living costs for two years</li></ul>'
      '<p><strong>Eligibility:</strong> outstanding academic record and leadership potential. '
      'Apply for both the master\'s and the MBA by the January round.</p>'),
    s('Cambridge Trust International Scholarships', 'Cambridge Trust, University of Cambridge', 'United Kingdom', 55000,
      date(2026, 9, 1), date(2026, 12, 3), 'https://www.cambridgetrust.org/',
      ['Master', 'PhD'], ANY, FULL, UNI, MERIT, EN, False,
      '<p>The Cambridge Trust funds hundreds of international students each year to study at Cambridge, '
      'often in partnership with colleges and departments.</p>'
      '<ul><li>Full or partial fees</li><li>Maintenance allowance</li></ul>'
      '<p><strong>Eligibility:</strong> international applicants to postgraduate courses. You are considered '
      'by completing the funding section of the Cambridge graduate application by the funding deadline.</p>'),
    s('LSE Graduate Support Scheme', 'London School of Economics and Political Science', 'United Kingdom', 20000,
      date(2026, 10, 1), date(2027, 4, 27), 'https://www.lse.ac.uk/study-at-lse/Graduate/fees-and-funding/Graduate-Support-Scheme',
      ['Master'], ['Social Sciences', 'Business'], PARTIAL, UNI, ['Need-based'], EN, False,
      '<p>Need-based awards from GBP 5,000 to GBP 15,000 for students on one-year master\'s programmes at LSE, '
      'the school\'s largest graduate funding scheme.</p>'
      '<ul><li>Tuition and living cost support</li></ul>'
      '<p><strong>Eligibility:</strong> an offer from LSE and demonstrated financial need. There are two '
      'rounds, the second usually closing in late April.</p>'),
    s('Felix Scholarships', 'The Felix Trust', 'United Kingdom', 50000,
      date(2026, 9, 1), date(2027, 1, 31), 'https://www.felixscholarship.org/',
      ['Master', 'PhD'], ANY, FULL, PRIV, ['Merit-based', 'Need-based'], EN, False,
      '<p>Full scholarships for gifted students from India and other developing countries to study at the '
      'University of Oxford, the University of Reading or SOAS University of London.</p>'
      '<ul><li>Tuition fees</li><li>Living stipend</li><li>Return airfare</li></ul>'
      '<p><strong>Eligibility:</strong> a first-class undergraduate degree and no means to fund study in the UK. '
      'Deadlines differ by university.</p>'),
    s("Warwick Chancellor's International Scholarships", 'University of Warwick', 'United Kingdom', 45000,
      date(2026, 9, 1), date(2027, 1, 15), 'https://warwick.ac.uk/services/dc/schols_fund/scholarships_and_funding/chancellorsint/',
      ['PhD'], ANY, FULL, UNI, ['Research'], EN, False,
      '<p>Around 25 fully funded PhD scholarships a year for top international research students at Warwick.</p>'
      '<ul><li>Full tuition fees</li><li>Annual maintenance stipend at UKRI rate</li></ul>'
      '<p><strong>Eligibility:</strong> overseas fee-paying PhD applicants nominated by their department. '
      'Apply for your PhD place early and ask to be considered.</p>'),

    # ---------------- United States ----------------
    s('Knight-Hennessy Scholars', 'Stanford University', 'United States', 90000,
      date(2027, 6, 1), date(2027, 10, 6), 'https://knight-hennessy.stanford.edu/',
      ['Master', 'PhD'], ANY, FULL, ['University', 'Private Foundation'], MERIT, ['TOEFL'], True,
      '<p>The largest fully endowed graduate scholarship in the world, funding up to 100 scholars a year '
      'for any graduate degree at Stanford plus a leadership programme.</p>'
      '<ul><li>Full tuition and fees</li><li>Living stipend</li><li>Travel and academic expenses</li></ul>'
      '<p><strong>Eligibility:</strong> applicants of any nationality who earned their bachelor\'s degree '
      'within the last seven years. Apply separately to Knight-Hennessy and to your Stanford programme.</p>'),
    s('AAUW International Fellowships', 'American Association of University Women', 'United States', 25000,
      date(2026, 8, 1), date(2026, 11, 15), 'https://www.aauw.org/resources/programs/fellowships-grants/current-opportunities/international/',
      ['Master', 'PhD'], ANY, PARTIAL, PRIV, MERIT, ['TOEFL'], False,
      '<p>Fellowships for women who are not US citizens or permanent residents to pursue full-time '
      'graduate or postdoctoral study in the United States.</p>'
      '<ul><li>USD 20,000 for master\'s</li><li>USD 25,000 for doctoral study</li></ul>'
      '<p><strong>Eligibility:</strong> women with a bachelor\'s degree who intend to return to their home '
      'country to pursue a professional career.</p>'),
    s('Hubert H. Humphrey Fellowship Program', 'U.S. Department of State', 'United States', 50000,
      date(2027, 3, 1), date(2027, 6, 1), 'https://www.humphreyfellowship.org/',
      ['Master'], ['Social Sciences', 'Business'], FULL, GOV, MERIT, ['TOEFL'], False,
      '<p>A Fulbright exchange programme bringing experienced mid-career professionals to the US for a year '
      'of non-degree graduate study, leadership development and professional work.</p>'
      '<ul><li>Tuition and fees</li><li>Monthly stipend</li><li>Health insurance</li><li>Travel</li></ul>'
      '<p><strong>Eligibility:</strong> at least five years of professional experience and an undergraduate '
      'degree. Run by the US embassy in each country; deadlines vary.</p>'),
    s('Joint Japan/World Bank Graduate Scholarship Program', 'World Bank and Government of Japan', 'United States', 45000,
      date(2027, 3, 1), date(2027, 5, 15), 'https://www.worldbank.org/en/programs/scholarships',
      ['Master'], ['Social Sciences', 'Business', 'Engineering'], FULL, ['Government'], ['Need-based'], EN, False,
      '<p>Scholarships for mid-career professionals from developing countries to study development-related '
      'master\'s programmes at partner universities in the US, Europe, Africa, Oceania and Japan.</p>'
      '<ul><li>Tuition</li><li>Monthly living allowance</li><li>Round-trip airfare</li><li>Health insurance</li></ul>'
      '<p><strong>Eligibility:</strong> nationals of World Bank member developing countries with at least three '
      'years of relevant work experience after their bachelor\'s.</p>'),
    s('East-West Center Graduate Degree Fellowship', 'East-West Center, Honolulu', 'United States', 40000,
      date(2026, 9, 1), date(2027, 1, 1), 'https://www.eastwestcenter.org/education/graduate-degree-fellowship',
      ['Master', 'PhD'], ANY, FULL, GOV, MERIT, ['TOEFL'], False,
      '<p>Fellowships for students from the Asia Pacific region and the US to study at the University of '
      'Hawai\'i at Manoa while taking part in the East-West Center\'s leadership programmes.</p>'
      '<ul><li>Housing at the Center</li><li>Stipend</li><li>Tuition support</li><li>Health insurance</li></ul>'
      '<p><strong>Eligibility:</strong> citizens of the US or Asia Pacific countries applying to a graduate '
      'programme at the University of Hawai\'i.</p>'),
    s('Rotary Peace Fellowship', 'Rotary International', 'United States', 50000,
      date(2027, 2, 1), date(2027, 5, 15), 'https://www.rotary.org/en/our-programs/peace-fellowships',
      ['Master'], ['Social Sciences'], FULL, PRIV, MERIT, EN, False,
      '<p>Fully funded fellowships for peace and development leaders to earn a master\'s degree or a '
      'professional certificate at Rotary Peace Centers at universities around the world.</p>'
      '<ul><li>Tuition and fees</li><li>Room and board</li><li>Round-trip transport</li>'
      '<li>Internship and field study expenses</li></ul>'
      '<p><strong>Eligibility:</strong> at least three years of related work experience for the master\'s '
      'programme. Applications close 15 May.</p>'),

    # ---------------- Canada ----------------
    s('UBC International Leader of Tomorrow Award', 'University of British Columbia', 'Canada', 50000,
      date(2026, 9, 1), date(2026, 12, 1), 'https://you.ubc.ca/financial-planning/scholarships-awards-international-students/',
      ['Bachelor'], ANY, FULL, UNI, ['Merit-based', 'Need-based'], EN, False,
      '<p>Need-based awards for outstanding international students entering an undergraduate degree at UBC, '
      'renewable for up to four years.</p>'
      '<ul><li>Tuition, fees and living costs based on financial need</li></ul>'
      '<p><strong>Eligibility:</strong> international secondary school students with strong grades, leadership '
      'and community involvement. Apply to UBC and submit the award application by early December.</p>'),
    s('Pierre Elliott Trudeau Foundation Doctoral Scholarships', 'Pierre Elliott Trudeau Foundation', 'Canada', 45000,
      date(2026, 9, 15), date(2026, 12, 3), 'https://www.trudeaufoundation.ca/',
      ['PhD'], ['Social Sciences'], FULL, PRIV, ['Research'], EN, False,
      '<p>Canada\'s most prestigious doctoral award in the social sciences and humanities, combining funding '
      'with a three-year leadership programme.</p>'
      '<ul><li>Up to CAD 40,000 a year for three years</li><li>Research and travel allowance</li></ul>'
      '<p><strong>Eligibility:</strong> Canadian citizens and foreign nationals enrolled, or applying, in a '
      'doctoral programme in the humanities or social sciences at a Canadian institution.</p>'),
    s('Mastercard Foundation Scholars Program', 'Mastercard Foundation and partner universities', 'Canada', 60000,
      date(2026, 9, 1), date(2027, 1, 31), 'https://mastercardfdn.org/en/what-we-do/our-programs/mastercard-foundation-scholars-program/',
      ['Bachelor', 'Master'], ANY, FULL, PRIV, ['Need-based'], EN, True,
      '<p>Comprehensive scholarships for academically talented young people from Africa with limited financial '
      'means, at partner universities in Canada, the US, Europe and Africa.</p>'
      '<ul><li>Tuition</li><li>Accommodation</li><li>Books and supplies</li><li>Travel</li>'
      '<li>Mentoring and career support</li></ul>'
      '<p><strong>Eligibility:</strong> citizens of African countries with financial need. Each partner university, '
      'such as the University of Toronto and UBC, runs its own application.</p>'),

    # ---------------- Ireland ----------------
    s('Mitchell Scholarship', 'US-Ireland Alliance', 'Ireland', 50000,
      date(2027, 6, 1), date(2027, 9, 28), 'https://www.us-irelandalliance.org/mitchellscholarship',
      ['Master'], ANY, FULL, PRIV, MERIT, [], False,
      '<p>Up to 12 Americans a year receive a year of postgraduate study at a university in Ireland or '
      'Northern Ireland.</p>'
      '<ul><li>Tuition</li><li>Accommodation</li><li>Living stipend</li><li>International travel</li></ul>'
      '<p><strong>Eligibility:</strong> US citizens aged 18 to 30 with a bachelor\'s degree, showing '
      'academic excellence, leadership and commitment to public service.</p>'),
    s('Government of Ireland International Education Scholarships', 'Higher Education Authority (Ireland)', 'Ireland',
      15000, date(2027, 1, 15), date(2027, 3, 12), 'https://hea.ie/policy/internationalisation/goi-ies/',
      ['Bachelor', 'Master', 'PhD'], ANY, PARTIAL, GOV, MERIT, EN, False,
      '<p>Scholarships for high-calibre international students to study in Ireland for one year at a '
      'participating Irish higher education institution.</p>'
      '<ul><li>EUR 10,000 stipend</li><li>Full tuition fee waiver</li></ul>'
      '<p><strong>Eligibility:</strong> non-EU/EEA students with an offer, or who have applied, to an '
      'Irish institution. Applications usually close in March.</p>'),

    # ---------------- France ----------------
    s('Eiffel Excellence Scholarship Programme', 'French Ministry for Europe and Foreign Affairs / Campus France',
      'France', 20000, date(2026, 10, 1), date(2027, 1, 8),
      'https://www.campusfrance.org/en/eiffel-scholarship-program-of-excellence',
      ['Master', 'PhD'], ['Engineering', 'Business', 'Social Sciences', 'Natural Sciences'], FULL, GOV, MERIT, EN, True,
      '<p>The French government\'s flagship scholarship to attract top international students to master\'s '
      'and PhD programmes at French higher education institutions.</p>'
      '<ul><li>Monthly allowance of about EUR 1,200 (master\'s)</li><li>Return travel</li>'
      '<li>Health insurance</li><li>Cultural activities</li></ul>'
      '<p><strong>Eligibility:</strong> non-French nationals under 30 (master\'s) or 35 (PhD). Applications '
      'are submitted by the French institution, not by students, usually by early January.</p>'),
    s('Emile Boutmy Scholarship', 'Sciences Po', 'France', 22000,
      date(2026, 10, 1), date(2026, 12, 1), 'https://www.sciencespo.fr/students/en/fees-funding/financial-aid/emile-boutmy-scholarship/',
      ['Bachelor', 'Master'], ['Social Sciences', 'Business'], PARTIAL, UNI, MERIT, EN, False,
      '<p>Sciences Po\'s merit scholarship for the best non-EU international students admitted to its '
      'undergraduate and master\'s programmes.</p>'
      '<ul><li>Tuition reduction from EUR 3,000 up to a full tuition waiver</li>'
      '<li>Additional living support for some recipients</li></ul>'
      '<p><strong>Eligibility:</strong> non-EU students applying to Sciences Po for the first time. You apply '
      'as part of the Sciences Po admission application.</p>'),
    s("Université Paris-Saclay International Master's Scholarships", 'Université Paris-Saclay', 'France', 13000,
      date(2026, 10, 15), date(2027, 3, 1), 'https://www.universite-paris-saclay.fr/en/admission/bourses-et-aides-financieres/international-masters-scholarships-program',
      ['Master'], STEM, PARTIAL, UNI, MERIT, EN, False,
      '<p>Scholarships for international students on master\'s programmes at Université Paris-Saclay, one of '
      'the top-ranked universities in Europe for mathematics and physics.</p>'
      '<ul><li>EUR 10,000 per year</li><li>Up to EUR 1,000 travel and visa costs</li></ul>'
      '<p><strong>Eligibility:</strong> excellent international students who did not live in France in the '
      'previous year. Apply through the master\'s admission platform.</p>'),

    # ---------------- Germany ----------------
    s('Heinrich Böll Foundation Scholarships', 'Heinrich Böll Stiftung', 'Germany', 14000,
      date(2027, 1, 15), date(2027, 3, 1), 'https://www.boell.de/en/scholarships',
      ['Master', 'PhD'], ANY, FULL, PRIV, ['Merit-based'], ['IELTS', 'TOEFL'], False,
      '<p>Scholarships for international students who are committed to the foundation\'s values of ecology, '
      'democracy, solidarity and non-violence, studying at German universities.</p>'
      '<ul><li>Monthly stipend of about EUR 992 (master\'s) or EUR 1,450 (PhD)</li><li>Health insurance</li>'
      '<li>Seminars and networking</li></ul>'
      '<p><strong>Eligibility:</strong> enrolled at, or applying to, a German university. Deadlines are '
      '1 March and 1 September.</p>'),
    s('Konrad-Adenauer-Stiftung Scholarships for International Students', 'Konrad-Adenauer-Stiftung', 'Germany', 14000,
      date(2026, 11, 1), date(2027, 1, 15), 'https://www.kas.de/en/web/begabtenfoerderung-und-kultur/foreign-students',
      ['Master', 'PhD'], ANY, FULL, PRIV, MERIT, [], False,
      '<p>Scholarships for highly qualified international graduates and doctoral candidates with social and '
      'political engagement, studying at German universities.</p>'
      '<ul><li>Monthly stipend</li><li>Health insurance</li><li>Seminar programme</li></ul>'
      '<p><strong>Eligibility:</strong> good German language skills are expected. Deadlines are 15 January '
      'and 15 July.</p>'),
    s('DAAD Development-Related Postgraduate Courses (EPOS)', 'German Academic Exchange Service (DAAD)', 'Germany', 14000,
      date(2026, 8, 1), date(2026, 12, 31), 'https://www.daad.de/en/studying-in-germany/scholarships/daad-scholarships/epos/',
      ['Master', 'PhD'], ['Engineering', 'Business', 'Social Sciences', 'Natural Sciences'], FULL, GOV, MERIT, EN, False,
      '<p>Full scholarships for professionals from developing countries to take selected development-related '
      'master\'s and PhD programmes at German universities.</p>'
      '<ul><li>Monthly stipend</li><li>Health, accident and liability insurance</li><li>Travel allowance</li>'
      '<li>German language course</li></ul>'
      '<p><strong>Eligibility:</strong> a bachelor\'s degree and at least two years of relevant work experience. '
      'Apply directly to the chosen programme; deadlines vary between August and December.</p>'),
    s('DAAD Research Grants - Doctoral Programmes in Germany', 'German Academic Exchange Service (DAAD)', 'Germany', 18000,
      date(2026, 8, 1), date(2026, 11, 30), 'https://www.daad.de/en/studying-in-germany/scholarships/daad-scholarships/',
      ['PhD'], ANY, FULL, GOV, ['Research'], EN, False,
      '<p>Scholarships for young researchers to complete a full doctoral degree at a German university or '
      'research institute.</p>'
      '<ul><li>Monthly stipend of EUR 1,300</li><li>Health insurance</li><li>Travel allowance</li>'
      '<li>Research allowance</li></ul>'
      '<p><strong>Eligibility:</strong> a master\'s degree completed within the last six years and a German '
      'supervisor. Deadlines depend on your home country.</p>'),
    s('DAAD Helmut-Schmidt-Programme (Public Policy and Good Governance)', 'German Academic Exchange Service (DAAD)',
      'Germany', 14000, date(2027, 5, 1), date(2027, 7, 31),
      'https://www.daad.de/en/studying-in-germany/scholarships/daad-scholarships/ppgg/',
      ['Master'], ['Social Sciences'], FULL, GOV, MERIT, EN, False,
      '<p>Scholarships for future leaders from developing countries to take master\'s programmes in public '
      'policy, governance and related fields at German universities.</p>'
      '<ul><li>Monthly stipend</li><li>Tuition fees covered where charged</li><li>Insurance and travel</li>'
      '<li>German language course</li></ul>'
      '<p><strong>Eligibility:</strong> graduates from eligible countries in Africa, Asia, Latin America and '
      'the Middle East. Deadlines are usually in July.</p>'),

    # ---------------- Netherlands ----------------
    s('Leiden University Excellence Scholarship (LExS)', 'Leiden University', 'Netherlands', 20000,
      date(2026, 10, 1), date(2027, 2, 1), 'https://www.universiteitleiden.nl/en/scholarships/sea/leiden-university-excellence-scholarship-lexs',
      ['Master'], ANY, PARTIAL, UNI, MERIT, EN, False,
      '<p>Scholarships for excellent non-EEA students applying to a master\'s programme at Leiden University.</p>'
      '<ul><li>EUR 10,000, EUR 15,000 or the full tuition fee minus the statutory fee</li></ul>'
      '<p><strong>Eligibility:</strong> students in the top 10% of their graduating class. Apply for your '
      'master\'s programme by 1 February.</p>'),
    s('Amsterdam Merit Scholarships', 'University of Amsterdam', 'Netherlands', 30000,
      date(2026, 10, 1), date(2027, 1, 15), 'https://www.uva.nl/en/education/fees-and-funding/scholarships-and-loans/amsterdam-merit-scholarships/amsterdam-merit-scholarships.html',
      ['Master'], ANY, ['Full Funding', 'Partial Funding'], UNI, MERIT, EN, False,
      '<p>Scholarships for talented international students from outside the EU/EEA for a master\'s programme '
      'at the University of Amsterdam.</p>'
      '<ul><li>Full scholarship of EUR 25,000 or partial EUR 12,500 to EUR 16,000</li></ul>'
      '<p><strong>Eligibility:</strong> excellent academic results (top 10% of the class). Apply through the '
      'master\'s application by mid-January.</p>'),
    s('Justus & Louise van Effen Excellence Scholarships', 'Delft University of Technology', 'Netherlands', 40000,
      date(2026, 10, 1), date(2026, 12, 1), 'https://www.tudelft.nl/en/education/practical-matters/scholarships/justus-louise-van-effen-excellence-scholarships',
      ['Master'], ['Engineering', 'Computer Science', 'Natural Sciences'], FULL, UNI, MERIT, EN, False,
      '<p>TU Delft\'s excellence scholarship for outstanding international students on its MSc programmes.</p>'
      '<ul><li>Full tuition fee</li><li>Living expenses for two years</li></ul>'
      '<p><strong>Eligibility:</strong> non-EEA students with a cumulative GPA of at least 80% of the scale '
      'maximum. Apply for your MSc by 1 December.</p>'),

    # ---------------- Switzerland ----------------
    s('ETH Zurich Excellence Scholarship & Opportunity Programme (ESOP)', 'ETH Zurich', 'Switzerland', 30000,
      date(2026, 11, 1), date(2026, 11, 30), 'https://ethz.ch/students/en/studies/financial/scholarships/excellencescholarship.html',
      ['Master'], ['Engineering', 'Computer Science', 'Natural Sciences'], FULL, UNI, MERIT, EN, True,
      '<p>ETH Zurich\'s top scholarship for outstanding students who want to take a master\'s degree at ETH.</p>'
      '<ul><li>Stipend covering living and study costs (about CHF 12,000 per semester)</li>'
      '<li>Tuition fee waiver</li><li>Mentoring by an ETH professor</li></ul>'
      '<p><strong>Eligibility:</strong> outstanding students in the top 10% of their bachelor\'s programme. '
      'Apply in the November master\'s window (deadline 30 November).</p>'),
    s('EPFL Excellence Fellowships', 'École Polytechnique Fédérale de Lausanne (EPFL)', 'Switzerland', 12000,
      date(2026, 11, 1), date(2026, 12, 15), 'https://www.epfl.ch/education/master/admission/excellence-fellowships/',
      ['Master'], ['Engineering', 'Computer Science', 'Natural Sciences'], PARTIAL, UNI, MERIT, EN, False,
      '<p>Fellowships for top students admitted to an EPFL master\'s programme.</p>'
      '<ul><li>CHF 10,000 per semester for the duration of the programme</li><li>Tuition waiver</li></ul>'
      '<p><strong>Eligibility:</strong> excellent academic record. Application is part of the master\'s '
      'admission; deadlines are 15 December and 15 April.</p>'),
    s("University of Geneva Excellence Master's Fellowships", 'University of Geneva', 'Switzerland', 15000,
      date(2026, 11, 1), date(2027, 3, 15), 'https://www.unige.ch/sciences/en/enseignements/formations/masters/excellencemasterfellowships/',
      ['Master'], ['Natural Sciences', 'Computer Science'], PARTIAL, UNI, MERIT, EN, False,
      '<p>Fellowships for outstanding students admitted to a master\'s programme at the Faculty of Science '
      'of the University of Geneva.</p>'
      '<ul><li>CHF 10,000 to CHF 15,000 per year</li><li>Tuition waiver</li></ul>'
      '<p><strong>Eligibility:</strong> students in the top 10% of their bachelor\'s programme. Applications '
      'usually close in mid-March.</p>'),

    # ---------------- Belgium ----------------
    s('VLIR-UOS Scholarships', 'VLIR-UOS (Flemish Interuniversity Council)', 'Belgium', 25000,
      date(2026, 11, 1), date(2027, 3, 1), 'https://www.vliruos.be/en/scholarships',
      ['Master'], ['Engineering', 'Natural Sciences', 'Social Sciences'], FULL, GOV, ['Need-based'], EN, False,
      '<p>Full scholarships for professionals from developing countries to take development-relevant '
      'master\'s and training programmes at Flemish universities.</p>'
      '<ul><li>Tuition</li><li>Monthly allowance</li><li>Accommodation</li><li>Travel and insurance</li></ul>'
      '<p><strong>Eligibility:</strong> nationals of one of the eligible VLIR-UOS countries with relevant '
      'work experience. Deadlines vary by programme, usually February to March.</p>'),
    s('Master Mind Scholarships (Flanders)', 'Flemish Government', 'Belgium', 13000,
      date(2026, 11, 1), date(2027, 3, 1), 'https://www.studyinflanders.be/scholarships/master-mind-scholarships',
      ['Master'], ANY, PARTIAL, GOV, MERIT, EN, False,
      '<p>Scholarships from the Flemish government for excellent international students to take a master\'s '
      'programme at a university or university college in Flanders or Brussels.</p>'
      '<ul><li>Up to EUR 8,400 grant</li><li>Tuition fee capped at EUR 1,099</li></ul>'
      '<p><strong>Eligibility:</strong> international students with excellent results. Apply through the '
      'Flemish institution, usually by early March.</p>'),
    s('Marie Skłodowska-Curie Doctoral Networks', 'European Commission', 'Belgium', 45000,
      date(2026, 9, 1), date(2027, 4, 30), 'https://marie-sklodowska-curie-actions.ec.europa.eu/',
      ['PhD'], STEM + ['Social Sciences'], FULL, GOV, ['Research'], EN, True,
      '<p>EU-funded paid PhD positions in international research networks across Europe, with excellent '
      'salaries and training.</p>'
      '<ul><li>Employment contract with competitive salary</li><li>Mobility allowance</li>'
      '<li>Family allowance where applicable</li></ul>'
      '<p><strong>Eligibility:</strong> open to all nationalities. You must not have lived in the host country '
      'for more than 12 months in the last three years. Positions open all year on EURAXESS.</p>'),
    s('KU Leuven Science@Leuven Scholarships', 'KU Leuven', 'Belgium', 12000,
      date(2026, 10, 1), date(2027, 3, 1), 'https://wet.kuleuven.be/english/scholarships',
      ['Master'], ['Natural Sciences', 'Engineering', 'Computer Science'], PARTIAL, UNI, MERIT, EN, False,
      '<p>Scholarships for excellent international students on master\'s programmes in science at KU Leuven, '
      'one of Europe\'s most innovative universities.</p>'
      '<ul><li>Tuition reduction to the standard EU rate</li><li>Living allowance for some recipients</li></ul>'
      '<p><strong>Eligibility:</strong> outstanding academic record; apply for admission by 1 March.</p>'),

    # ---------------- Nordics ----------------
    s('Danish Government Scholarships', 'Danish Ministry of Higher Education and Science', 'Denmark', 25000,
      date(2026, 11, 1), date(2027, 3, 1), 'https://studyindenmark.dk/tuition-fees-scholarships/scholarships',
      ['Master'], ANY, ['Full Funding', 'Partial Funding'], GOV, MERIT, EN, False,
      '<p>Tuition waivers and living grants for highly qualified non-EU/EEA students in full-degree '
      'programmes at Danish universities.</p>'
      '<ul><li>Full or partial tuition waiver</li><li>Living grant for some students</li></ul>'
      '<p><strong>Eligibility:</strong> non-EU/EEA students. Each university selects recipients and sets its '
      'deadline (usually 15 January or 1 March).</p>'),
    s('Aalto University Scholarships', 'Aalto University', 'Finland', 18000,
      date(2026, 12, 1), date(2027, 1, 4), 'https://www.aalto.fi/en/study-at-aalto/scholarships-and-tuition-fees',
      ['Master'], ['Engineering', 'Business', 'Computer Science'], ['Full Funding', 'Partial Funding'], UNI, MERIT, EN, False,
      '<p>Aalto scholarships cover 50% or 100% of tuition for top non-EU/EEA students in master\'s programmes, '
      'with some awards including a living grant.</p>'
      '<ul><li>50% or 100% tuition waiver</li><li>EUR 10,000 grant for some recipients</li></ul>'
      '<p><strong>Eligibility:</strong> students required to pay tuition fees in Finland. Apply in the '
      'December to January admission round.</p>'),
    s('University of Helsinki Scholarships', 'University of Helsinki', 'Finland', 20000,
      date(2026, 12, 1), date(2027, 1, 7), 'https://www.helsinki.fi/en/admissions-and-education/apply-masters-programmes/scholarships-and-grants',
      ['Master'], ANY, ['Full Funding', 'Partial Funding'], UNI, MERIT, EN, False,
      '<p>Scholarships for excellent fee-paying students on international master\'s programmes at the '
      'University of Helsinki.</p>'
      '<ul><li>Tuition waiver (100% or 50%)</li><li>EUR 10,000 living grant (full scholarship)</li></ul>'
      '<p><strong>Eligibility:</strong> students from outside the EU/EEA. Apply in the master\'s admission '
      'round in December and January.</p>'),
    s('Uppsala University Global Scholarships', 'Uppsala University', 'Sweden', 18000,
      date(2026, 10, 15), date(2027, 1, 15), 'https://www.uu.se/en/study/scholarships',
      ['Master'], ANY, PARTIAL, UNI, MERIT, EN, False,
      '<p>Scholarships covering tuition fees for top fee-paying students on master\'s programmes at Uppsala, '
      'Sweden\'s oldest university.</p>'
      '<ul><li>Partial or full tuition fee coverage</li></ul>'
      '<p><strong>Eligibility:</strong> students required to pay tuition in Sweden. Apply for admission by '
      'mid-January and submit the scholarship application by early February.</p>'),
    s('Lund University Global Scholarship', 'Lund University', 'Sweden', 18000,
      date(2026, 10, 15), date(2027, 2, 1), 'https://www.lunduniversity.lu.se/admissions/bachelors-masters-studies/scholarships-awards/lund-university-global-scholarship-programme',
      ['Bachelor', 'Master'], ANY, PARTIAL, UNI, MERIT, EN, False,
      '<p>Scholarships for top academic students from outside the EU/EEA applying to Lund University.</p>'
      '<ul><li>Tuition fee reduction of 25%, 50%, 75% or 100%</li></ul>'
      '<p><strong>Eligibility:</strong> applicants required to pay tuition. Apply for admission by mid-January '
      'and for the scholarship by 1 February.</p>'),
    s('KTH Scholarship', 'KTH Royal Institute of Technology', 'Sweden', 35000,
      date(2026, 10, 15), date(2027, 1, 15), 'https://www.kth.se/en/studies/master/admission/scholarships',
      ['Master'], ['Engineering', 'Computer Science', 'Natural Sciences'], FULL, UNI, MERIT, EN, False,
      '<p>A highly competitive scholarship covering the full tuition fee for the full master\'s programme '
      'at KTH in Stockholm.</p>'
      '<ul><li>Full tuition fee for two years</li></ul>'
      '<p><strong>Eligibility:</strong> fee-paying students with excellent study results. Apply for '
      'your programme by mid-January.</p>'),

    # ---------------- Italy and Spain ----------------
    s('Italian Government Scholarships for International Students', 'Italian Ministry of Foreign Affairs (MAECI)',
      'Italy', 12000, date(2027, 2, 1), date(2027, 5, 31), 'https://studyinitaly.esteri.it/en/call-for-procedure',
      ['Master', 'PhD'], ANY, PARTIAL, GOV, MERIT, [], False,
      '<p>Scholarships from the Italian government for international students to study at Italian '
      'universities, art and music institutions.</p>'
      '<ul><li>Monthly allowance of EUR 900</li><li>Tuition exemption at many universities</li>'
      '<li>Health insurance</li></ul>'
      '<p><strong>Eligibility:</strong> foreign citizens and Italian citizens resident abroad. '
      'Apply online on the Study in Italy portal.</p>'),
    s('University of Bologna Study Grants for International Students', 'University of Bologna', 'Italy', 13000,
      date(2027, 1, 15), date(2027, 3, 31), 'https://www.unibo.it/en/study/scholarships-and-grants/unibo-action-1-2',
      ['Bachelor', 'Master'], ANY, PARTIAL, UNI, MERIT, EN, False,
      '<p>Study grants at the world\'s oldest university for international students with excellent records.</p>'
      '<ul><li>Grant of about EUR 11,000</li><li>Tuition fee exemption</li></ul>'
      '<p><strong>Eligibility:</strong> students with a foreign qualification applying for a first or second '
      'cycle degree. Calls usually open in January.</p>'),
    s('Bocconi International Awards', 'Bocconi University', 'Italy', 20000,
      date(2026, 9, 15), date(2027, 3, 15), 'https://www.unibocconi.it/en/programs/funding-and-scholarships',
      ['Bachelor', 'Master'], ['Business', 'Social Sciences'], ['Full Funding', 'Partial Funding'], UNI, MERIT, EN, False,
      '<p>Merit awards for outstanding international students admitted to Bocconi\'s bachelor\'s and master\'s '
      'programmes in Milan.</p>'
      '<ul><li>Full or partial tuition waiver</li><li>Cash award of up to EUR 12,000 per year</li></ul>'
      '<p><strong>Eligibility:</strong> non-Italian applicants; you are considered automatically when you apply '
      'in one of the admission rounds.</p>'),
    s('Fundación Carolina Scholarships', 'Fundación Carolina', 'Spain', 18000,
      date(2027, 1, 15), date(2027, 3, 15), 'https://www.fundacioncarolina.es/en/',
      ['Master', 'PhD'], ANY, ['Full Funding', 'Partial Funding'], ['Government', 'Private Foundation'], MERIT, [], False,
      '<p>Scholarships for students from Latin America and Portugal to take postgraduate studies at Spanish '
      'universities and business schools.</p>'
      '<ul><li>Tuition</li><li>Monthly living allowance</li><li>Return flight</li><li>Medical insurance</li></ul>'
      '<p><strong>Eligibility:</strong> nationals of Latin American countries in the Ibero-American community. '
      'Programmes are taught in Spanish.</p>'),

    # ---------------- Central and Eastern Europe ----------------
    s('Ernst Mach Grant (Worldwide)', 'OeAD - Austria\'s Agency for Education and Internationalisation', 'Austria', 14000,
      date(2026, 12, 1), date(2027, 3, 1), 'https://oead.at/en/to-austria/grants-and-scholarships',
      ['PhD'], ANY, PARTIAL, GOV, ['Research'], EN, False,
      '<p>Research grants for young researchers from around the world to carry out doctoral or postdoctoral '
      'research at an Austrian university.</p>'
      '<ul><li>Monthly grant of EUR 1,150 (pre-doc)</li><li>Accommodation support</li><li>Insurance</li></ul>'
      '<p><strong>Eligibility:</strong> graduate researchers with an Austrian host. Apply on the OeAD scholarship '
      'database; deadlines vary.</p>'),
    s('ISTA Graduate School PhD Program', 'Institute of Science and Technology Austria (ISTA)', 'Austria', 35000,
      date(2026, 10, 1), date(2027, 1, 8), 'https://ista.ac.at/en/education/application/',
      ['PhD'], STEM, FULL, ['University'], ['Research'], EN, False,
      '<p>Fully funded PhD positions at one of Europe\'s leading basic research institutes, near Vienna.</p>'
      '<ul><li>Full employment contract with a competitive salary</li><li>No tuition fees</li>'
      '<li>Social security and benefits</li></ul>'
      '<p><strong>Eligibility:</strong> a bachelor\'s or master\'s degree in a science field. All nationalities '
      'welcome; deadline in early January.</p>'),
    s('Stipendium Hungaricum Scholarship', 'Tempus Public Foundation, Government of Hungary', 'Hungary', 12000,
      date(2026, 11, 1), date(2027, 1, 15), 'https://stipendiumhungaricum.hu/',
      ['Bachelor', 'Master', 'PhD'], ANY, FULL, GOV, MERIT, EN, True,
      '<p>The Hungarian government\'s flagship scholarship, funding around 5,000 international students a '
      'year at Hungarian universities.</p>'
      '<ul><li>Tuition-free education</li><li>Monthly stipend</li><li>Accommodation or housing allowance</li>'
      '<li>Medical insurance</li></ul>'
      '<p><strong>Eligibility:</strong> citizens of one of the 90+ partner countries, nominated by their '
      'sending partner. Applications close in mid-January.</p>'),
    s('Türkiye Burslari Scholarships', 'Presidency for Turks Abroad and Related Communities (YTB)', 'Turkey', 10000,
      date(2027, 1, 10), date(2027, 2, 20), 'https://www.turkiyeburslari.gov.tr/',
      ['Bachelor', 'Master', 'PhD'], ANY, FULL, GOV, MERIT, [], True,
      '<p>Turkey\'s government-funded, highly competitive scholarship programme for international students '
      'at top Turkish universities.</p>'
      '<ul><li>Tuition fees</li><li>Monthly stipend</li><li>Accommodation</li><li>Health insurance</li>'
      '<li>Round-trip flight</li><li>One-year Turkish language course</li></ul>'
      '<p><strong>Eligibility:</strong> students of all nationalities meeting age and grade requirements. '
      'Applications usually run from January to 20 February.</p>'),
    s('Russian Government Scholarship (Education Quota)', 'Ministry of Science and Higher Education, Russian Federation',
      'Russia', 8000, date(2026, 9, 15), date(2027, 1, 15), 'https://education-in-russia.com/',
      ['Bachelor', 'Master', 'PhD'], ANY, FULL, GOV, MERIT, [], False,
      '<p>Government quota places for international students to study at Russian state universities free of charge.</p>'
      '<ul><li>Full tuition</li><li>Preparatory Russian language year</li><li>Monthly stipend</li>'
      '<li>Dormitory place</li></ul>'
      '<p><strong>Eligibility:</strong> foreign citizens. Apply on the Education in Russia portal; deadlines are '
      'usually mid-December for CIS countries and mid-January for others.</p>'),

    # ---------------- China and Hong Kong ----------------
    s('Schwarzman Scholars', 'Schwarzman Scholars, Tsinghua University', 'China', 80000,
      date(2027, 4, 1), date(2027, 9, 15), 'https://www.schwarzmanscholars.org/',
      ['Master'], ['Social Sciences', 'Business'], FULL, ['Private Foundation', 'University'], MERIT, EN, True,
      '<p>A one-year master\'s in Global Affairs at Tsinghua University in Beijing, designed to prepare '
      'future leaders for a world shaped by China.</p>'
      '<ul><li>Tuition and fees</li><li>Room and board</li><li>Travel to and from Beijing</li>'
      '<li>Study tour</li><li>Personal stipend</li></ul>'
      '<p><strong>Eligibility:</strong> aged 18 to 28 with a bachelor\'s degree. The international deadline '
      'is usually in mid-September.</p>'),
    s('Yenching Academy Scholarship', 'Yenching Academy, Peking University', 'China', 30000,
      date(2026, 9, 1), date(2026, 12, 4), 'https://yenchingacademy.pku.edu.cn/',
      ['Master'], ['Social Sciences'], FULL, UNI, MERIT, EN, False,
      '<p>Fully funded interdisciplinary master\'s in China Studies at Peking University, for exceptional '
      'graduates from around the world.</p>'
      '<ul><li>Tuition</li><li>Accommodation</li><li>Monthly stipend</li><li>Round-trip airfare</li></ul>'
      '<p><strong>Eligibility:</strong> a bachelor\'s degree, usually under 28, with a strong interest in China. '
      'Deadline in early December.</p>'),
    s('Chinese MOFCOM Scholarship', 'Ministry of Commerce of the People\'s Republic of China', 'China', 15000,
      date(2027, 2, 1), date(2027, 4, 30), 'https://www.campuschina.org/',
      ['Master', 'PhD'], ['Business', 'Social Sciences', 'Engineering'], FULL, GOV, MERIT, EN, False,
      '<p>Full scholarships for government officials and professionals from developing countries to take '
      'master\'s and PhD programmes at Chinese universities, taught in English.</p>'
      '<ul><li>Tuition</li><li>Accommodation</li><li>Living allowance</li><li>Round-trip airfare</li>'
      '<li>Medical insurance</li></ul>'
      '<p><strong>Eligibility:</strong> applicants from developing countries, usually with work experience. '
      'Apply through the Chinese embassy or economic and commercial office.</p>'),
    s('Hong Kong PhD Fellowship Scheme', 'Research Grants Council of Hong Kong', 'Hong Kong', 46000,
      date(2026, 9, 1), date(2026, 12, 1), 'https://cerg1.ugc.edu.hk/hkpfs/index.html',
      ['PhD'], ANY, FULL, GOV, ['Research'], EN, True,
      '<p>Around 400 fellowships a year for the best students worldwide to pursue PhD studies at Hong Kong\'s '
      'leading universities.</p>'
      '<ul><li>Annual stipend of HK$344,400</li><li>Conference and research travel allowance of HK$14,400</li>'
      '<li>Tuition waiver at many universities</li></ul>'
      '<p><strong>Eligibility:</strong> students of any nationality applying to a PhD programme at a UGC-funded '
      'university. Deadline is 1 December at noon Hong Kong time.</p>'),

    # ---------------- Japan, Korea, Taiwan ----------------
    s('OIST Graduate School PhD Program', 'Okinawa Institute of Science and Technology', 'Japan', 40000,
      date(2026, 10, 1), date(2026, 12, 15), 'https://admissions.oist.jp/',
      ['PhD'], STEM, FULL, ['University'], ['Research'], EN, False,
      '<p>A fully funded five-year interdisciplinary PhD programme in science, taught entirely in English, '
      'at one of the world\'s top research institutes.</p>'
      '<ul><li>Tuition fully covered</li><li>Research assistantship of about JPY 3 million per year</li>'
      '<li>Housing support</li><li>Travel to Japan</li></ul>'
      '<p><strong>Eligibility:</strong> a bachelor\'s degree in any science discipline; all nationalities '
      'welcome. Main deadline in mid-December.</p>'),
    s('ADB-Japan Scholarship Program', 'Asian Development Bank', 'Japan', 30000,
      date(2026, 11, 1), date(2027, 3, 31), 'https://www.adb.org/work-with-us/careers/japan-scholarship-program',
      ['Master'], ['Business', 'Social Sciences', 'Engineering'], FULL, GOV, MERIT, EN, False,
      '<p>Scholarships for nationals of ADB developing member countries to study development-related '
      'master\'s programmes at participating institutions in Asia and the Pacific.</p>'
      '<ul><li>Tuition</li><li>Monthly subsistence and housing allowance</li><li>Books and travel</li>'
      '<li>Medical insurance</li></ul>'
      '<p><strong>Eligibility:</strong> at least two years of full-time work experience and age 35 or under. '
      'Apply to the participating university, which nominates candidates.</p>'),
    s('Ashinaga Africa Initiative', 'Ashinaga', 'Japan', 30000,
      date(2026, 11, 1), date(2027, 1, 31), 'https://ashinaga.org/en/programs/ashinaga-africa-initiative/',
      ['Bachelor'], ANY, FULL, PRIV, ['Need-based'], EN, False,
      '<p>Full undergraduate scholarships for orphaned students from Sub-Saharan Africa to study at universities '
      'around the world, with a leadership programme.</p>'
      '<ul><li>Tuition</li><li>Accommodation and living expenses</li><li>Travel</li><li>Leadership training</li></ul>'
      '<p><strong>Eligibility:</strong> students from Sub-Saharan Africa who have lost one or both parents.</p>'),
    s('KAIST International Student Scholarship', 'Korea Advanced Institute of Science and Technology', 'South Korea', 15000,
      date(2026, 10, 1), date(2027, 1, 15), 'https://admission.kaist.ac.kr/intl-undergraduate/',
      ['Bachelor', 'Master', 'PhD'], STEM, FULL, UNI, MERIT, EN, False,
      '<p>Scholarships for international students admitted to KAIST, Korea\'s top science and technology university.</p>'
      '<ul><li>Full tuition</li><li>Monthly allowance</li><li>Health insurance</li></ul>'
      '<p><strong>Eligibility:</strong> international applicants admitted to KAIST. There are several rounds '
      'each year, typically closing in autumn and winter.</p>'),
    s('Taiwan Scholarship', 'Ministry of Education, Taiwan', 'Taiwan', 12000,
      date(2027, 2, 1), date(2027, 3, 31), 'https://taiwanscholarship.moe.gov.tw/',
      ['Bachelor', 'Master', 'PhD'], ANY, FULL, GOV, MERIT, [], False,
      '<p>Taiwan government scholarships for international students to study degree programmes at Taiwanese '
      'universities.</p>'
      '<ul><li>Tuition and fees up to NTD 40,000 per semester</li><li>Monthly stipend of NTD 15,000 to 20,000</li></ul>'
      '<p><strong>Eligibility:</strong> foreign nationals with excellent results. Apply through the Taiwan '
      'representative office in your country between February and March.</p>'),
    s('Taiwan ICDF International Higher Education Scholarship', 'International Cooperation and Development Fund (Taiwan ICDF)',
      'Taiwan', 15000, date(2027, 1, 1), date(2027, 3, 31), 'https://www.icdf.org.tw/',
      ['Bachelor', 'Master', 'PhD'], ['Engineering', 'Business', 'Social Sciences', 'Natural Sciences'], FULL, GOV, MERIT, EN, False,
      '<p>Full scholarships for students from partner countries to take English-taught programmes at '
      'Taiwanese universities.</p>'
      '<ul><li>Airfare</li><li>Tuition and credit fees</li><li>Accommodation</li><li>Monthly stipend</li>'
      '<li>Insurance</li></ul>'
      '<p><strong>Eligibility:</strong> citizens of Taiwan ICDF partner countries, recommended by their government.</p>'),

    # ---------------- Singapore and South / Southeast Asia ----------------
    s('Singapore International Graduate Award (SINGA)', 'A*STAR, NUS, NTU and SUTD', 'Singapore', 30000,
      date(2026, 10, 1), date(2026, 12, 1), 'https://www.a-star.edu.sg/Scholarships/for-graduate-studies/singapore-international-graduate-award-singa',
      ['PhD'], STEM, FULL, ['Government', 'University'], ['Research'], EN, True,
      '<p>Four-year PhD scholarships for international students to research in science and engineering in Singapore.</p>'
      '<ul><li>Full tuition</li><li>Monthly stipend of SGD 2,700 (rising after qualifying exam)</li>'
      '<li>One-time airfare and settling-in allowance</li></ul>'
      '<p><strong>Eligibility:</strong> international graduates with a passion for research. Intakes in January '
      'and August with deadlines on 1 June and 1 December.</p>'),
    s('ASEAN Undergraduate Scholarship', 'National University of Singapore / Nanyang Technological University', 'Singapore',
      25000, date(2026, 10, 1), date(2027, 2, 28), 'https://www.nus.edu.sg/oam/scholarships',
      ['Bachelor'], ANY, PARTIAL, UNI, MERIT, EN, False,
      '<p>Scholarships for top students from ASEAN member countries (excluding Singapore) to study undergraduate '
      'degrees at NUS or NTU.</p>'
      '<ul><li>Tuition fees after Tuition Grant</li><li>Annual living allowance</li><li>Accommodation allowance</li></ul>'
      '<p><strong>Eligibility:</strong> ASEAN citizens with excellent results and leadership. You are considered '
      'when you apply for admission.</p>'),
    s('NUS Research Scholarship', 'National University of Singapore', 'Singapore', 30000,
      date(2026, 8, 1), date(2026, 11, 15), 'https://nusgs.nus.edu.sg/scholarships/',
      ['PhD'], ANY, FULL, UNI, ['Research'], EN, False,
      '<p>Research scholarships for outstanding graduates to take a PhD at the National University of Singapore, '
      'Asia\'s top-ranked university.</p>'
      '<ul><li>Full tuition</li><li>Monthly stipend</li></ul>'
      '<p><strong>Eligibility:</strong> open to all nationalities. You are considered when you apply for a PhD; '
      'deadlines are usually in mid-November and mid-May.</p>'),
    s('ICCR Scholarship Schemes', 'Indian Council for Cultural Relations', 'India', 6000,
      date(2027, 1, 1), date(2027, 3, 31), 'https://a2ascholarships.iccr.gov.in/',
      ['Bachelor', 'Master', 'PhD'], ANY, FULL, GOV, MERIT, [], False,
      '<p>The Government of India\'s scholarship schemes for international students at Indian universities '
      'and institutes.</p>'
      '<ul><li>Tuition fees</li><li>Monthly stipend</li><li>House rent allowance</li><li>Contingency grant</li></ul>'
      '<p><strong>Eligibility:</strong> nationals of eligible countries. Apply through the A2A portal and the '
      'Indian mission in your country.</p>'),

    # ---------------- Middle East ----------------
    s('MBZUAI Graduate Scholarship', 'Mohamed bin Zayed University of Artificial Intelligence', 'United Arab Emirates',
      45000, date(2026, 9, 1), date(2026, 12, 15), 'https://mbzuai.ac.ae/admissions/',
      ['Master', 'PhD'], ['Computer Science'], FULL, UNI, MERIT, EN, False,
      '<p>Full scholarships for every admitted student at the world\'s first graduate-level AI university, in Abu Dhabi.</p>'
      '<ul><li>Full tuition</li><li>Monthly stipend</li><li>Accommodation</li><li>Health insurance</li>'
      '<li>Visa sponsorship</li></ul>'
      '<p><strong>Eligibility:</strong> a strong degree in computer science, engineering, mathematics or a related '
      'field. Priority deadline is usually in December.</p>'),
    s('KAUST Fellowship', 'King Abdullah University of Science and Technology', 'Saudi Arabia', 45000,
      date(2026, 9, 1), date(2027, 1, 15), 'https://admissions.kaust.edu.sa/',
      ['Master', 'PhD'], STEM, FULL, UNI, MERIT, EN, False,
      '<p>All admitted master\'s and PhD students at KAUST receive a full fellowship to study at one of the '
      'world\'s fastest-rising research universities.</p>'
      '<ul><li>Full tuition</li><li>Living stipend</li><li>Free housing</li><li>Medical and dental coverage</li>'
      '<li>Relocation support</li></ul>'
      '<p><strong>Eligibility:</strong> open to all nationalities with a strong academic record. Main deadline '
      'is 15 January for autumn entry.</p>'),

    # ---------------- Australia and New Zealand ----------------
    s('Melbourne Research Scholarship', 'University of Melbourne', 'Australia', 30000,
      date(2027, 1, 1), date(2027, 3, 31), 'https://scholarships.unimelb.edu.au/awards/graduate-research-scholarships',
      ['Master', 'PhD'], ANY, FULL, UNI, ['Research'], ['IELTS'], False,
      '<p>Graduate research scholarships for domestic and international students at Australia\'s top-ranked university.</p>'
      '<ul><li>Living allowance of about AUD 37,000 per year</li><li>Full fee offset</li>'
      '<li>Overseas Student Health Cover</li><li>Relocation grant</li></ul>'
      '<p><strong>Eligibility:</strong> applicants with a strong research background. You are considered '
      'automatically when you apply for a graduate research degree.</p>'),
    s("ANU Chancellor's International Scholarship", 'Australian National University', 'Australia', 15000,
      date(2026, 8, 1), date(2026, 12, 15), 'https://www.anu.edu.au/study/scholarships',
      ['Bachelor', 'Master'], ANY, PARTIAL, UNI, MERIT, ['IELTS'], False,
      '<p>Merit scholarships for high-achieving international students at the Australian National University.</p>'
      '<ul><li>Tuition reduction of 25% to 50% for the duration of the programme</li></ul>'
      '<p><strong>Eligibility:</strong> international students with an offer to ANU and an outstanding academic '
      'record. Considered automatically with your application.</p>'),
    s('Monash International Leadership Scholarship', 'Monash University', 'Australia', 35000,
      date(2026, 9, 1), date(2027, 1, 31), 'https://www.monash.edu/study/fees-scholarships/scholarships/find-a-scholarship/monash-international-leadership-scholarship-5642',
      ['Bachelor', 'Master'], ANY, FULL, UNI, MERIT, ['IELTS'], False,
      '<p>Full tuition scholarships for international students with academic excellence and leadership.</p>'
      '<ul><li>100% tuition fees for the full degree</li></ul>'
      '<p><strong>Eligibility:</strong> international students with a strong record and demonstrated leadership. '
      'There are rounds for each intake.</p>'),
    s('UNSW Scientia PhD Scholarship', 'University of New South Wales', 'Australia', 35000,
      date(2026, 9, 1), date(2027, 3, 31), 'https://www.scholarships.unsw.edu.au/scholarships/id/1385',
      ['PhD'], ANY, FULL, UNI, ['Research'], ['IELTS'], False,
      '<p>UNSW\'s prestigious PhD scholarship with a generous stipend and a career development package.</p>'
      '<ul><li>Stipend of about AUD 50,000 per year</li><li>Tuition fees</li>'
      '<li>Up to AUD 10,000 per year for career development</li></ul>'
      '<p><strong>Eligibility:</strong> outstanding candidates of any nationality applying to listed Scientia '
      'projects. Several rounds per year.</p>'),
    s('Manaaki New Zealand Scholarships', 'New Zealand Ministry of Foreign Affairs and Trade', 'New Zealand', 40000,
      date(2027, 3, 1), date(2027, 3, 31), 'https://www.nzscholarships.govt.nz/',
      ['Master', 'PhD'], ANY, FULL, GOV, ['Merit-based', 'Need-based'], ['IELTS'], False,
      '<p>New Zealand government scholarships for people from eligible Pacific, Asian, African and Latin '
      'American countries to study at New Zealand universities.</p>'
      '<ul><li>Full tuition</li><li>Living allowance</li><li>Establishment allowance</li><li>Travel</li>'
      '<li>Medical insurance</li></ul>'
      '<p><strong>Eligibility:</strong> citizens of eligible countries committed to returning home. The '
      'application window is usually during March.</p>'),
    s('University of Auckland International Student Excellence Scholarship', 'University of Auckland', 'New Zealand',
      12000, date(2026, 9, 1), date(2026, 12, 1), 'https://www.auckland.ac.nz/en/study/scholarships-and-awards.html',
      ['Bachelor', 'Master'], ANY, PARTIAL, UNI, MERIT, ['IELTS'], False,
      '<p>Scholarships for excellent international students starting a degree at New Zealand\'s top-ranked university.</p>'
      '<ul><li>Tuition award of up to NZD 20,000</li></ul>'
      '<p><strong>Eligibility:</strong> international students with an offer and an outstanding academic record. '
      'Rounds open for each intake.</p>'),

    # ---------------- Other global ----------------
    s('Aga Khan Foundation International Scholarship Programme', 'Aga Khan Foundation', 'Switzerland', 30000,
      date(2027, 1, 1), date(2027, 3, 31), 'https://the.akdn/en/how-we-work/our-agencies/aga-khan-foundation/international-scholarship-programme',
      ['Master', 'PhD'], ANY, ['Full Funding', 'Partial Funding'], PRIV, ['Need-based', 'Merit-based'], EN, False,
      '<p>Postgraduate scholarships for outstanding students from selected developing countries who cannot '
      'otherwise fund their studies, at reputable universities worldwide.</p>'
      '<ul><li>Tuition and living expenses on a 50% grant and 50% loan basis</li></ul>'
      '<p><strong>Eligibility:</strong> nationals of Bangladesh, Egypt, India, Kenya, Madagascar, Mozambique, '
      'Pakistan, Syria, Tajikistan, Tanzania, Uganda and other eligible countries, under 30.</p>'),
    s('Jardine Scholarship', 'Jardine Foundation', 'United Kingdom', 60000,
      date(2027, 7, 1), date(2027, 10, 31), 'https://www.jardines.com/en/community/jardine-foundation',
      ['Bachelor', 'Master'], ANY, FULL, PRIV, MERIT, EN, False,
      '<p>Full scholarships for outstanding students from Southeast and East Asia to study at the University '
      'of Oxford or the University of Cambridge.</p>'
      '<ul><li>University and college fees</li><li>Maintenance allowance</li><li>Return flights</li></ul>'
      '<p><strong>Eligibility:</strong> citizens of Hong Kong, Malaysia, Singapore, Indonesia, the Philippines, '
      'Thailand, Vietnam, Myanmar and Cambodia.</p>'),
    s('Yale University International Financial Aid', 'Yale University', 'United States', 85000,
      date(2026, 8, 1), date(2027, 1, 2), 'https://finaid.yale.edu/',
      ['Bachelor'], ANY, FULL, UNI, ['Need-based'], ['TOEFL'], False,
      '<p>Yale admits international students need-blind and meets 100% of their demonstrated financial need '
      'with grants, not loans.</p>'
      '<ul><li>Need-based grants covering tuition, housing, food and travel</li><li>No loans in aid packages</li></ul>'
      '<p><strong>Eligibility:</strong> all admitted undergraduates, regardless of citizenship. Regular decision '
      'deadline is 2 January.</p>'),
    s('MIT Undergraduate Financial Aid for International Students', 'Massachusetts Institute of Technology', 'United States',
      85000, date(2026, 8, 1), date(2027, 1, 5), 'https://sfs.mit.edu/',
      ['Bachelor'], STEM, FULL, UNI, ['Need-based'], ['TOEFL'], False,
      '<p>MIT admits international students need-blind and meets the full demonstrated financial need of '
      'every admitted student.</p>'
      '<ul><li>Need-based MIT Scholarship covering tuition, housing and living costs</li></ul>'
      '<p><strong>Eligibility:</strong> all admitted undergraduates. Families earning under USD 200,000 '
      'typically pay no tuition. Regular action deadline in early January.</p>'),
    s('Harvard University Financial Aid for International Students', 'Harvard College', 'United States', 85000,
      date(2026, 8, 1), date(2027, 1, 1), 'https://college.harvard.edu/financial-aid',
      ['Bachelor'], ANY, FULL, UNI, ['Need-based'], ['TOEFL'], True,
      '<p>Harvard meets 100% of demonstrated need for all admitted students, including international students, '
      'with grants and no loans.</p>'
      '<ul><li>Grants covering tuition, room, board and travel based on need</li></ul>'
      '<p><strong>Eligibility:</strong> all admitted undergraduates. Families with lower incomes typically pay '
      'nothing. Regular decision deadline is 1 January.</p>'),
    s('Oxford Reach Oxford Scholarship', 'University of Oxford', 'United Kingdom', 50000,
      date(2026, 9, 1), date(2027, 2, 10), 'https://www.ox.ac.uk/admissions/undergraduate/fees-and-funding/oxford-support/reach-oxford-scholarship',
      ['Bachelor'], ANY, FULL, UNI, ['Need-based'], EN, False,
      '<p>Scholarships for students from low-income countries who cannot study for a degree in their home country '
      'because of political or financial reasons.</p>'
      '<ul><li>Course fees</li><li>Grant for living costs</li><li>One return airfare per year</li></ul>'
      '<p><strong>Eligibility:</strong> students from eligible countries with an offer for an undergraduate '
      'course at Oxford.</p>'),
]
