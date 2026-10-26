from datetime import date

# Corrections to the first 100 scholarships after checking each against its official page (October 2026).
# Keyed by the original title; a 'title' value renames the entry. Only the listed fields are overridden.

CORRECTIONS = {
    'Chevening Scholarships': {
        # The 2027-28 round closed in early October 2026
        'open_date': date(2027, 8, 5),
        'deadline': date(2027, 10, 6),
    },
    "Commonwealth Master's Scholarships": {
        'open_date': date(2027, 8, 1),
        'deadline': date(2027, 10, 19),
        'description': (
            "<p>Fully funded one-year master's study in the UK for students from low and middle income "
            'Commonwealth countries who could not otherwise afford to study in the UK.</p>'
            '<ul><li>Full tuition fees</li><li>Return airfare</li>'
            '<li>Stipend of GBP 1,712 per month (GBP 2,000 in London)</li><li>Study travel grant</li></ul>'
            '<p><strong>Eligibility:</strong> citizen of, and resident in, an eligible Commonwealth country, with at '
            'least an upper second-class (2:1) degree and no previous UK master\'s. Apply through your national '
            'nominating agency or a selected NGO, which set earlier deadlines. The 2027-28 round closed on '
            '20 October 2026.</p>'
        ),
    },
    'Swedish Institute Scholarships for Global Professionals': {
        'open_date': date(2027, 2, 8),
        'deadline': date(2027, 2, 24),
        'description': (
            "<p>Full scholarships for professionals from 34 eligible countries to take a master's programme at a "
            'Swedish university.</p>'
            '<ul><li>Tuition fees</li><li>Living expenses</li><li>Travel grant</li><li>Insurance</li></ul>'
            '<p><strong>Eligibility:</strong> citizens of eligible countries, including Bangladesh, Egypt, Ethiopia, '
            'Kenya, Nigeria, Rwanda, Senegal, South Africa, Tanzania, Uganda and Zambia, with at least 3,000 hours '
            "of work experience. Apply to an eligible master's programme by 15 January 2027, then to SI between "
            '8 and 24 February 2027.</p>'
        ),
    },
    'Swiss Government Excellence Scholarships': {
        'amount': 32000,
        'description': (
            '<p>Research scholarships for early-career researchers from abroad to do a PhD or postdoctoral research '
            'at a Swiss university or federal institute of technology.</p>'
            '<ul><li>CHF 2,450 per month</li><li>Tuition exemption</li><li>Health insurance</li></ul>'
            "<p><strong>Eligibility:</strong> a completed master's degree, aged 35 or under, from one of 183 eligible "
            'countries, with a Swiss host professor. Applications opened 20 August 2026; deadlines are set per '
            'country through the Swiss embassy (mostly November-December).</p>'
        ),
    },
    'Holland Scholarship': {
        'title': 'NL Scholarship (formerly Holland Scholarship)',
        'amount': 5400,
        'description': (
            "<p>A one-off EUR 5,000 award (formerly the Holland Scholarship) for non-EEA students starting a "
            "full-time bachelor's or master's at a participating Dutch institution.</p>"
            '<ul><li>EUR 5,000 paid in the first year of study</li></ul>'
            '<p><strong>Eligibility:</strong> non-EEA nationality and no previous degree from a Dutch institution. '
            'Each institution sets its own deadline, often 1 February or 1 May.</p>'
        ),
    },
    'Commonwealth PhD Scholarships': {
        'application_url': 'https://cscuk.fcdo.gov.uk/scholarships/commonwealth-phd-scholarships-for-least-developed-countries-and-vulnerable-states/',
    },
    'Commonwealth Shared Scholarships': {
        'application_url': 'https://cscuk.fcdo.gov.uk/scholarships/commonwealth-shared-scholarships-applications/',
    },
    'Eiffel Excellence Scholarship Programme': {
        'deadline': date(2027, 1, 6),
        'description': (
            "<p>The French government's flagship scholarship to attract top international students to master's "
            'and PhD programmes at French higher education institutions.</p>'
            '<ul><li>Monthly allowance</li><li>Return travel</li><li>Health insurance</li><li>Cultural activities</li></ul>'
            "<p><strong>Eligibility:</strong> non-French nationals aged up to 29 (master's) or 35 (PhD). Only French "
            'institutions can submit applications; Campus France must receive them by 6 January 2027, with results '
            'from 12 April 2027.</p>'
        ),
    },
    'Emile Boutmy Scholarship': {
        'application_url': 'https://www.sciencespo.fr/students/en/fees-funding/bursaries-financial-aid/emile-boutmy-scholarship/',
        'description': (
            "<p>Sciences Po's merit scholarship for outstanding non-EEA students applying to its undergraduate and "
            "master's programmes, awarded to around 300 students a year.</p>"
            '<ul><li>Tuition reduction (amount depends on the profile)</li></ul>'
            '<p><strong>Eligibility:</strong> first-time applicants from outside the European Economic Area, selected '
            'on merit and profile. You are considered as part of the Sciences Po admission application.</p>'
        ),
    },
    'Leiden University Excellence Scholarship (LExS)': {
        'deadline': date(2026, 12, 1),
        'description': (
            "<p>Partial tuition scholarships for excellent non-EEA students applying to a master's programme at "
            'Leiden University.</p>'
            '<ul><li>EUR 10,000, 15,000, 17,500, 18,500 or 19,000 towards tuition</li></ul>'
            "<p><strong>Eligibility:</strong> non-EEA passport holders starting a full-time master's in September, "
            'roughly in the top 10% of their previous programme. Apply for admission, then submit the LExS '
            'application with a motivation letter by 1 December 2026.</p>'
        ),
    },
    'Amsterdam Merit Scholarships': {
        'application_url': 'https://www.uva.nl/en/education/fees-and-funding/masters-scholarships-and-loans/amsterdam-merit-scholarship/amsterdam-merit-scholarship.html',
        'amount': 0,
        'description': (
            "<p>Scholarships for outstanding students from outside the EU/EEA who plan to take a master's programme "
            'at the University of Amsterdam.</p>'
            '<ul><li>Tuition support (amount set by each faculty)</li></ul>'
            "<p><strong>Eligibility:</strong> non-EU/EEA passport holders who have applied for a UvA master's. "
            "Deadlines differ by faculty or graduate school; apply through that school's admissions office.</p>"
        ),
    },
    'Justus & Louise van Effen Excellence Scholarships': {
        'application_url': 'https://www.tudelft.nl/en/education/study-programme-orientation/practical-matters/scholarships',
        'description': (
            "<p>TU Delft's excellence scholarship for outstanding international students on its two-year MSc "
            'programmes.</p>'
            '<ul><li>Full tuition fees for the first year</li><li>Contribution towards living expenses</li>'
            '<li>Second-year support if at least 48 of 60 ECTS are completed</li></ul>'
            '<p><strong>Eligibility:</strong> excellent international applicants (roughly top 10%) conditionally '
            'admitted to a regular two-year MSc. Submit the scholarship form, a reference letter and an English '
            'certificate by 1 December 2026.</p>'
        ),
    },
    'EPFL Excellence Fellowships': {
        'application_url': 'https://www.epfl.ch/education/master/master-excellence-fellowships/',
        'amount': 22600,
        'description': (
            "<p>Fellowships for outstanding students admitted to an EPFL master's programme.</p>"
            '<ul><li>CHF 10,000 per semester</li><li>Guaranteed housing</li></ul>'
            "<p><strong>Eligibility:</strong> strong academic results plus achievements in areas such as sport, arts, "
            "civic life or entrepreneurship. Apply in the first master's window by 15 December (EPFL bachelor's "
            'students by 31 January). Renewal needs 50 ECTS and a 5.0/6 average.</p>'
        ),
    },
    'Master Mind Scholarships (Flanders)': {
        'description': (
            "<p>Flemish government scholarships for excellent international students to take a master's programme "
            'at a university or university college in Flanders or Brussels.</p>'
            '<ul><li>Grant plus reduced tuition (amounts are being confirmed while the scheme is reorganised)</li></ul>'
            '<p><strong>Eligibility:</strong> international students with excellent results and a degree from outside '
            'Flanders. The scheme is being reorganised, so check with your chosen institution for the 2027 call.</p>'
        ),
    },
    'KU Leuven Science@Leuven Scholarships': {
        'application_url': 'https://wet.kuleuven.be/english/scienceatleuvenscholarship/',
        'description': (
            "<p>Scholarships for international students on master's programmes in the Faculty of Science at "
            'KU Leuven.</p>'
            '<ul><li>Tuition reduction and allowance (see the official page for amounts)</li></ul>'
            "<p><strong>Eligibility:</strong> international applicants to eligible science master's programmes. The "
            '2026-27 round is closed; check the faculty page for the 2027-28 call.</p>'
        ),
    },
    'Danish Government Scholarships': {
        'application_url': 'https://studyindenmark.dk/study-options/scholarships',
        'description': (
            '<p>Danish State tuition fee waivers and scholarships for non-EU/EEA students on full-degree programmes, '
            'awarded by each Danish university.</p>'
            '<ul><li>Full or partial tuition fee waiver</li><li>Grant towards living costs for some students</li></ul>'
            '<p><strong>Eligibility:</strong> citizens of countries outside the EU/EEA and Switzerland with a residence '
            'permit for education. Each university selects recipients and sets its own deadline.</p>'
        ),
    },
    'Aalto University Scholarships': {
        'application_url': 'https://www.aalto.fi/en/admission-services/scholarships-and-tuition-fees',
        'amount': 18000,
        'fund_types': ['Full Funding'],
        'description': (
            "<p>The Aalto University Excellence Scholarship waives the full tuition fee for top non-EU/EEA master's "
            'students. Awards are very limited and some programmes may award none.</p>'
            '<ul><li>100% tuition fee waiver for the two-year programme (fees are EUR 15,000-20,000 a year)</li>'
            '<li>Living costs are not covered</li></ul>'
            "<p><strong>Eligibility:</strong> fee-paying students with excellent results. Apply on the master's "
            'application form during the admission round (December-January).</p>'
        ),
    },
    'University of Helsinki Scholarships': {
        'application_url': 'https://www.helsinki.fi/en/admissions-and-education/apply-bachelors-and-masters-programmes/tuition-fees-and-scholarship-programme',
        'amount': 7500,
        'fund_types': ['Partial Funding', 'Full Funding'],
        'description': (
            "<p>Tuition fee waivers for excellent fee-paying students on international master's programmes at the "
            'University of Helsinki.</p>'
            '<ul><li>50% or 100% tuition waiver for two years (most awards are 50%)</li>'
            '<li>Fees are EUR 13,000, 15,000 or 18,000 a year; living costs are not covered</li></ul>'
            "<p><strong>Eligibility:</strong> non-EU/EEA applicants liable for fees with excellent results. Select the "
            "waiver option on the master's application form (December-January); keep 55 ECTS a year.</p>"
        ),
    },
    'Uppsala University Global Scholarships': {
        'application_url': 'https://www.uu.se/en/study/masters-studies/scholarships/uppsala-university-scholarships',
        'open_date': date(2027, 1, 16),
        'deadline': date(2027, 2, 1),
        'amount': 15000,
        'fund_types': ['Full Funding'],
        'description': (
            "<p>The Uppsala University Global Scholarship covers the full tuition fee for an international master's "
            "programme at Sweden's oldest university.</p>"
            '<ul><li>Full tuition fee (living costs not covered)</li></ul>'
            "<p><strong>Eligibility:</strong> citizens of countries outside the EU/EEA and Switzerland, with the Uppsala "
            'programme as first priority. Apply for admission by 15 January 2027, then for the scholarship between '
            '16 January and 1 February 2027.</p>'
        ),
    },
    'Lund University Global Scholarship': {
        'application_url': 'https://www.lunduniversity.lu.se/study/admission-degree-studies/scholarships-and-awards/lund-university-global-scholarship',
        'deadline': date(2027, 2, 15),
        'amount': 0,
        'description': (
            '<p>Merit scholarships for top non-EU/EEA students applying to Lund University.</p>'
            '<ul><li>Covers part or all of the tuition fee (depends on the programme or faculty budget)</li></ul>'
            "<p><strong>Eligibility:</strong> fee-paying applicants to a master's (or selected bachelor's) programme "
            'with Lund as first choice. Apply for admission by 15 January; the scholarship portal opens in early '
            'February (last deadline 16 February 2026).</p>'
        ),
    },
    'Italian Government Scholarships for International Students': {
        'application_url': 'https://studyinitaly.esteri.it/ListaBandi',
    },
    'Bocconi International Awards': {
        'application_url': 'https://www.unibocconi.it/en/applying-bocconi/master-science-and-ma-programs/funding/bocconi-graduate-merit-awards-ay-2026-27',
        'title': 'Bocconi Graduate Merit Awards',
        'levels': ['Master'],
        'fund_types': ['Full Funding'],
        'description': (
            "<p>Merit awards for top applicants to Bocconi's MSc programmes in Milan, including international "
            'students.</p>'
            '<ul><li>100% waiver of tuition and fees</li><li>Renewed for the second year with 50 credits</li></ul>'
            '<p><strong>Eligibility:</strong> top applicants in each admission round; no separate application. Awards '
            'are announced with admission results, mostly in the first rounds.</p>'
        ),
    },
    'ISTA Graduate School PhD Program': {
        'application_url': 'https://phd.pages.ista.ac.at/apply/',
    },
    'Ashinaga Africa Initiative': {
        'application_url': 'https://www.ashinaga.org/activity/africa-support/aai/',
    },
    'Singapore International Graduate Award (SINGA)': {
        'application_url': 'https://www.a-star.edu.sg/Scholarships',
    },
    "ANU Chancellor's International Scholarship": {
        'title': 'ANU International Achievement Award',
        'application_url': 'https://study.anu.edu.au/scholarships/find-scholarship/anu-international-achievement-award',
        'description': (
            '<p>An automatic tuition scholarship for high-achieving international students at the Australian '
            'National University.</p>'
            '<ul><li>Up to 50% off tuition for up to four years</li></ul>'
            '<p><strong>Eligibility:</strong> international applicants to ANU coursework programmes; considered '
            'automatically with no separate application. ANU also offers a 20% first-year Vice-Chancellor\'s '
            'International Achievement Award.</p>'
        ),
    },
}
