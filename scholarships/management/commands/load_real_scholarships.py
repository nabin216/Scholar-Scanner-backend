from datetime import date
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from scholarships.models import (
    Scholarship, Country, Level, ScholarshipCategory,
    FieldOfStudy, FundType, SponsorType, LanguageRequirement
)

from ._more_scholarships import MORE_SCHOLARSHIPS

# One 1200x675 photo per scholarship, named after slugify(title). Sources and licences: seed_images/CREDITS.md
SEED_IMAGES = Path(__file__).resolve().parents[2] / 'seed_images'

NOTE = (
    '<p><em>Deadlines and amounts change every cycle and can differ by country. '
    'Always confirm the current details on the official website before applying.</em></p>'
)

# Deadlines are the expected next application deadline; amount is an approximate yearly value in USD.
SCHOLARSHIPS = [
    {
        'title': 'Chevening Scholarships',
        'provider': 'UK Foreign, Commonwealth & Development Office',
        'country': 'United Kingdom',
        'amount': 45000,
        'open_date': date(2026, 8, 5),
        'deadline': date(2026, 11, 4),
        'application_url': 'https://www.chevening.org/scholarships/',
        'levels': ['Master'],
        'fields': ['Any Field'],
        'fund_types': ['Full Funding'],
        'sponsors': ['Government'],
        'categories': ['Merit-based'],
        'languages': ['IELTS', 'TOEFL'],
        'featured': True,
        'description': (
            "<p>The UK government's flagship scholarship for future leaders. Covers a one-year "
            "master's degree at any UK university.</p>"
            '<ul><li>Full tuition fees</li><li>Monthly living stipend</li>'
            '<li>Return economy flight to the UK</li><li>Visa and arrival allowances</li></ul>'
            '<p><strong>Eligibility:</strong> citizen of a Chevening-eligible country, an undergraduate '
            'degree, at least two years of work experience, and a commitment to return home for two '
            'years after the award.</p>'
        ),
    },
    {
        'title': "Commonwealth Master's Scholarships",
        'provider': 'Commonwealth Scholarship Commission in the UK',
        'country': 'United Kingdom',
        'amount': 40000,
        'open_date': date(2026, 9, 15),
        'deadline': date(2026, 12, 15),
        'application_url': 'https://cscuk.fcdo.gov.uk/scholarships/commonwealth-masters-scholarships/',
        'levels': ['Master'],
        'fields': ['Any Field'],
        'fund_types': ['Full Funding'],
        'sponsors': ['Government'],
        'categories': ['Merit-based', 'Need-based'],
        'languages': ['IELTS'],
        'featured': False,
        'description': (
            "<p>Fully funded one-year master's study in the UK for students from low and "
            'middle income Commonwealth countries who could not otherwise afford to study in the UK.</p>'
            '<ul><li>Tuition fees</li><li>Return airfare</li><li>Monthly stipend</li>'
            '<li>Thesis and arrival allowances</li></ul>'
            '<p><strong>Eligibility:</strong> citizen of an eligible Commonwealth country with at least '
            'an upper second-class (2:1) undergraduate degree. Apply through your national nominating agency.</p>'
        ),
    },
    {
        'title': 'Rhodes Scholarship',
        'provider': 'Rhodes Trust, University of Oxford',
        'country': 'United Kingdom',
        'amount': 70000,
        'open_date': date(2027, 6, 1),
        'deadline': date(2027, 7, 31),
        'application_url': 'https://www.rhodeshouse.ox.ac.uk/scholarships/the-rhodes-scholarship/',
        'levels': ['Master', 'PhD'],
        'fields': ['Any Field'],
        'fund_types': ['Full Funding'],
        'sponsors': ['Private Foundation'],
        'categories': ['Merit-based'],
        'languages': ['IELTS', 'TOEFL'],
        'featured': True,
        'description': (
            "<p>The world's oldest international graduate scholarship, for postgraduate study at the "
            'University of Oxford.</p>'
            '<ul><li>All university and college fees</li><li>Annual living stipend</li>'
            '<li>Travel to and from Oxford</li></ul>'
            '<p><strong>Eligibility:</strong> typically aged 18-24 (up to 27 in some constituencies), '
            'outstanding academic record, leadership and commitment to service. Deadlines vary by '
            'country, mostly between July and October.</p>'
        ),
    },
    {
        'title': 'Gates Cambridge Scholarship',
        'provider': 'Gates Cambridge Trust, University of Cambridge',
        'country': 'United Kingdom',
        'amount': 60000,
        'open_date': date(2026, 9, 1),
        'deadline': date(2026, 12, 3),
        'application_url': 'https://www.gatescambridge.org/',
        'levels': ['Master', 'PhD'],
        'fields': ['Any Field'],
        'fund_types': ['Full Funding'],
        'sponsors': ['Private Foundation'],
        'categories': ['Merit-based'],
        'languages': ['IELTS', 'TOEFL'],
        'featured': True,
        'description': (
            '<p>Full-cost scholarships for outstanding applicants from outside the UK to pursue a '
            'full-time postgraduate degree at the University of Cambridge.</p>'
            '<ul><li>University composition fee</li><li>Maintenance allowance</li>'
            '<li>Airfare and visa costs</li><li>Discretionary family and academic development funding</li></ul>'
            '<p><strong>Eligibility:</strong> non-UK citizens applying for a full-time postgraduate '
            'degree. Apply through the Cambridge graduate application and tick the Gates box. '
            'US applicants have an earlier deadline in October.</p>'
        ),
    },
    {
        'title': 'Fulbright Foreign Student Program',
        'provider': 'U.S. Department of State',
        'country': 'United States',
        'amount': 50000,
        'open_date': date(2026, 12, 1),
        'deadline': date(2027, 2, 15),
        'application_url': 'https://foreign.fulbrightonline.org/',
        'levels': ['Master', 'PhD'],
        'fields': ['Any Field'],
        'fund_types': ['Full Funding'],
        'sponsors': ['Government'],
        'categories': ['Merit-based'],
        'languages': ['TOEFL'],
        'featured': True,
        'description': (
            "<p>The U.S. government's flagship exchange program for graduate students, young "
            'professionals and artists to study and research in the United States.</p>'
            '<ul><li>Tuition</li><li>Airfare</li><li>Living stipend</li><li>Health insurance</li></ul>'
            '<p><strong>Eligibility:</strong> run by the U.S. Embassy or Fulbright Commission in each '
            'country. Requirements and deadlines differ by country, usually between February and October.</p>'
        ),
    },
    {
        'title': 'DAAD Study Scholarships for Graduates',
        'provider': 'German Academic Exchange Service (DAAD)',
        'country': 'Germany',
        'amount': 14000,
        'open_date': date(2026, 8, 1),
        'deadline': date(2026, 11, 15),
        'application_url': 'https://www2.daad.de/deutschland/stipendium/datenbank/en/21148-scholarship-database/',
        'levels': ['Master'],
        'fields': ['Any Field'],
        'fund_types': ['Full Funding'],
        'sponsors': ['Government'],
        'categories': ['Merit-based'],
        'languages': ['IELTS', 'TOEFL'],
        'featured': False,
        'description': (
            "<p>Scholarships for international graduates to complete a master's degree at a German "
            'state or state-recognised university.</p>'
            '<ul><li>Monthly stipend (around EUR 992)</li><li>Health insurance</li>'
            '<li>Travel allowance</li><li>Possible German language course</li></ul>'
            '<p><strong>Eligibility:</strong> a bachelor\'s degree completed within the last six years. '
            'Most German public universities charge no tuition. Deadlines depend on your country and field.</p>'
        ),
    },
    {
        'title': "Erasmus Mundus Joint Master's Scholarships",
        'provider': 'European Commission',
        'country': 'Belgium',
        'amount': 30000,
        'open_date': date(2026, 10, 1),
        'deadline': date(2027, 1, 15),
        'application_url': 'https://www.eacea.ec.europa.eu/scholarships/erasmus-mundus-catalogue_en',
        'levels': ['Master'],
        'fields': ['Engineering', 'Computer Science', 'Business', 'Social Sciences', 'Natural Sciences'],
        'fund_types': ['Full Funding'],
        'sponsors': ['Government'],
        'categories': ['Merit-based'],
        'languages': ['IELTS', 'TOEFL'],
        'featured': True,
        'description': (
            "<p>EU-funded scholarships for joint master's programmes taught by a consortium of "
            'universities, with study in at least two European countries.</p>'
            '<ul><li>Full participation (tuition) costs</li><li>Monthly allowance of about EUR 1,400</li>'
            '<li>Travel and installation costs</li></ul>'
            '<p><strong>Eligibility:</strong> open to students worldwide with a bachelor\'s degree. '
            'You apply directly to each programme in the catalogue, and each sets its own deadline.</p>'
        ),
    },
    {
        'title': 'Australia Awards Scholarships',
        'provider': 'Australian Government, Department of Foreign Affairs and Trade',
        'country': 'Australia',
        'amount': 55000,
        'open_date': date(2027, 2, 1),
        'deadline': date(2027, 4, 30),
        'application_url': 'https://www.dfat.gov.au/people-to-people/australia-awards/australia-awards-scholarships',
        'levels': ['Bachelor', 'Master', 'PhD'],
        'fields': ['Any Field'],
        'fund_types': ['Full Funding'],
        'sponsors': ['Government'],
        'categories': ['Merit-based', 'Need-based'],
        'languages': ['IELTS'],
        'featured': False,
        'description': (
            '<p>Long-term development awards for people from eligible countries in the Indo-Pacific, '
            'Africa and the Middle East to study at Australian universities.</p>'
            '<ul><li>Full tuition fees</li><li>Return air travel</li><li>Establishment allowance</li>'
            '<li>Contribution to living expenses</li><li>Overseas Student Health Cover</li></ul>'
            '<p><strong>Eligibility:</strong> citizen of a participating country, not holding Australian '
            'residency, and willing to return home for two years after study.</p>'
        ),
    },
    {
        'title': 'MEXT Japanese Government Scholarship',
        'provider': 'Ministry of Education, Culture, Sports, Science and Technology (Japan)',
        'country': 'Japan',
        'amount': 15000,
        'open_date': date(2027, 4, 1),
        'deadline': date(2027, 5, 31),
        'application_url': 'https://www.studyinjapan.go.jp/en/smap-stopj-applications-scholarship.html',
        'levels': ['Bachelor', 'Master', 'PhD'],
        'fields': ['Any Field'],
        'fund_types': ['Full Funding'],
        'sponsors': ['Government'],
        'categories': ['Merit-based'],
        'languages': [],
        'featured': False,
        'description': (
            '<p>Japanese government scholarships for international students at Japanese universities, '
            'through embassy or university recommendation.</p>'
            '<ul><li>Tuition and admission fees waived</li><li>Monthly stipend of about JPY 117,000-145,000</li>'
            '<li>Round-trip airfare</li></ul>'
            '<p><strong>Eligibility:</strong> nationals of countries with diplomatic relations with Japan. '
            'Embassy recommendation deadlines are usually between April and June.</p>'
        ),
    },
    {
        'title': 'Global Korea Scholarship (GKS)',
        'provider': 'National Institute for International Education (NIIED), Korea',
        'country': 'South Korea',
        'amount': 20000,
        'open_date': date(2027, 2, 1),
        'deadline': date(2027, 3, 15),
        'application_url': 'https://www.studyinkorea.go.kr/',
        'levels': ['Bachelor', 'Master', 'PhD'],
        'fields': ['Any Field'],
        'fund_types': ['Full Funding'],
        'sponsors': ['Government'],
        'categories': ['Merit-based'],
        'languages': [],
        'featured': False,
        'description': (
            '<p>Korean government scholarship for international students to study at Korean universities, '
            'including a one-year Korean language course.</p>'
            '<ul><li>Full tuition</li><li>Monthly living allowance</li><li>Round-trip airfare</li>'
            '<li>Korean language training</li><li>Medical insurance</li></ul>'
            '<p><strong>Eligibility:</strong> applicants and their parents must not hold Korean citizenship. '
            'Graduate applications usually open in February; undergraduate in September.</p>'
        ),
    },
    {
        'title': 'Chinese Government Scholarship (CSC)',
        'provider': 'China Scholarship Council',
        'country': 'China',
        'amount': 12000,
        'open_date': date(2027, 1, 1),
        'deadline': date(2027, 3, 31),
        'application_url': 'https://www.campuschina.org/',
        'levels': ['Bachelor', 'Master', 'PhD'],
        'fields': ['Any Field'],
        'fund_types': ['Full Funding'],
        'sponsors': ['Government'],
        'categories': ['Merit-based'],
        'languages': [],
        'featured': False,
        'description': (
            '<p>Scholarships from the Chinese Ministry of Education for international students at '
            'designated Chinese universities, through embassies or directly through universities.</p>'
            '<ul><li>Tuition waiver</li><li>On-campus accommodation</li>'
            '<li>Monthly stipend (CNY 2,500-3,500)</li><li>Medical insurance</li></ul>'
            '<p><strong>Eligibility:</strong> non-Chinese citizens in good health. Age limits apply '
            '(under 25 for bachelor, 35 for master, 40 for PhD).</p>'
        ),
    },
    {
        'title': 'Swedish Institute Scholarships for Global Professionals',
        'provider': 'Swedish Institute',
        'country': 'Sweden',
        'amount': 35000,
        'open_date': date(2027, 2, 10),
        'deadline': date(2027, 2, 25),
        'application_url': 'https://si.se/en/apply/scholarships/swedish-institute-scholarships-for-global-professionals/',
        'levels': ['Master'],
        'fields': ['Any Field'],
        'fund_types': ['Full Funding'],
        'sponsors': ['Government'],
        'categories': ['Merit-based'],
        'languages': ['IELTS', 'TOEFL'],
        'featured': False,
        'description': (
            "<p>Scholarships for professionals from selected countries to take a master's programme "
            'at a Swedish university.</p>'
            '<ul><li>Tuition fees</li><li>Living expenses of SEK 12,000 per month</li>'
            '<li>Travel grant</li><li>Insurance</li></ul>'
            '<p><strong>Eligibility:</strong> citizen of an eligible country, at least 3,000 hours of '
            'work experience, and admission to an eligible master\'s programme. Apply for university '
            'admission first (deadline mid-January).</p>'
        ),
    },
    {
        'title': 'Lester B. Pearson International Scholarship',
        'provider': 'University of Toronto',
        'country': 'Canada',
        'amount': 65000,
        'open_date': date(2026, 9, 1),
        'deadline': date(2027, 1, 15),
        'application_url': 'https://future.utoronto.ca/pearson/about/',
        'levels': ['Bachelor'],
        'fields': ['Any Field'],
        'fund_types': ['Full Funding'],
        'sponsors': ['University'],
        'categories': ['Merit-based'],
        'languages': ['IELTS', 'TOEFL'],
        'featured': True,
        'description': (
            '<p>The University of Toronto\'s most prestigious award for international undergraduate '
            'students who show exceptional academic achievement and creativity.</p>'
            '<ul><li>Tuition</li><li>Books and incidental fees</li>'
            '<li>Full residence support for four years</li></ul>'
            '<p><strong>Eligibility:</strong> international students in their final year of secondary '
            'school who must be nominated by their school (nomination deadline is usually early November).</p>'
        ),
    },
    {
        'title': 'Swiss Government Excellence Scholarships',
        'provider': 'Swiss Confederation (FCS)',
        'country': 'Switzerland',
        'amount': 26000,
        'open_date': date(2026, 8, 1),
        'deadline': date(2026, 12, 15),
        'application_url': 'https://www.sbfi.admin.ch/sbfi/en/home/education/scholarships-and-grants/swiss-government-excellence-scholarships.html',
        'levels': ['PhD'],
        'fields': ['Any Field'],
        'fund_types': ['Full Funding'],
        'sponsors': ['Government'],
        'categories': ['Research'],
        'languages': ['IELTS', 'TOEFL'],
        'featured': False,
        'description': (
            '<p>Research scholarships for PhD and postdoctoral researchers at Swiss universities and '
            'federal institutes of technology.</p>'
            '<ul><li>Monthly stipend of CHF 1,920</li><li>Tuition exemption</li>'
            '<li>Health insurance</li><li>Housing allowance</li></ul>'
            '<p><strong>Eligibility:</strong> a master\'s degree and a Swiss host professor who supports '
            'your research. Applications go through the Swiss embassy in your country; deadlines vary.</p>'
        ),
    },
    {
        'title': 'Holland Scholarship',
        'provider': 'Dutch Ministry of Education and Dutch research universities',
        'country': 'Netherlands',
        'amount': 5400,
        'open_date': date(2026, 11, 1),
        'deadline': date(2027, 2, 1),
        'application_url': 'https://www.studyinnl.org/finances/holland-scholarship',
        'levels': ['Bachelor', 'Master'],
        'fields': ['Any Field'],
        'fund_types': ['Partial Funding'],
        'sponsors': ['Government', 'University'],
        'categories': ['Merit-based'],
        'languages': ['IELTS', 'TOEFL'],
        'featured': False,
        'description': (
            '<p>A one-off EUR 5,000 award for international students from outside the European Economic '
            'Area starting a bachelor\'s or master\'s at a participating Dutch university.</p>'
            '<ul><li>EUR 5,000 paid in the first year of study</li></ul>'
            '<p><strong>Eligibility:</strong> non-EEA nationality and no previous degree from a Dutch '
            'institution. Deadline is 1 February for most programmes (1 May for some).</p>'
        ),
    },
]


class Command(BaseCommand):
    help = (
        'Load the real, well-known international scholarships. Creates missing ones and attaches '
        'missing images; existing data is only overwritten with --update.'
    )

    def add_arguments(self, parser):
        parser.add_argument('--update', action='store_true', help='Overwrite existing scholarships with this data')

    def handle(self, *args, **options):
        created = updated = images = 0
        all_scholarships = SCHOLARSHIPS + MORE_SCHOLARSHIPS
        for data in all_scholarships:
            scholarship = Scholarship.objects.filter(title=data['title']).first()
            is_new = scholarship is None
            if is_new or options['update']:
                scholarship = scholarship or Scholarship(title=data['title'])
                scholarship.provider = data['provider']
                scholarship.country = Country.objects.get_or_create(name=data['country'])[0]
                scholarship.amount = data['amount']
                scholarship.open_date = data['open_date']
                scholarship.deadline = data['deadline']
                scholarship.application_url = data['application_url']
                scholarship.is_featured = data['featured']
                scholarship.description = data['description'] + NOTE
                scholarship.save()
                scholarship.levels.set([Level.objects.get_or_create(name=n)[0] for n in data['levels']])
                scholarship.field_of_study.set([FieldOfStudy.objects.get_or_create(name=n)[0] for n in data['fields']])
                scholarship.fund_type.set([FundType.objects.get_or_create(name=n)[0] for n in data['fund_types']])
                scholarship.sponsor_type.set([SponsorType.objects.get_or_create(name=n)[0] for n in data['sponsors']])
                scholarship.scholarship_category.set(
                    [ScholarshipCategory.objects.get_or_create(name=n)[0] for n in data['categories']]
                )
                scholarship.language_requirement.set(
                    [LanguageRequirement.objects.get_or_create(name=n)[0] for n in data['languages']]
                )
                created += is_new
                updated += not is_new

            image_path = SEED_IMAGES / f"{slugify(data['title'])}.jpg"
            if not scholarship.image and image_path.exists():
                with image_path.open('rb') as f:
                    scholarship.image.save(image_path.name, File(f), save=True)
                images += 1

        self.stdout.write(self.style.SUCCESS(
            f'Done: {created} created, {updated} updated, {images} images attached '
            f'({len(all_scholarships)} scholarships)'
        ))
