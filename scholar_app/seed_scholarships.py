
from datetime import date

from django.core.management.base import BaseCommand
from scholar_app.models import Scholarship


class Command(BaseCommand):
    help = "Add verified National Scholarship Portal scheme entries"

    def handle(self, *args, **options):

        deadline = date(2026, 11, 30)

        schemes = [
            {
                "title": "AICTE Pragati Scholarship Scheme for Girl Students - Technical Degree",
                "provider": "AICTE, Government of India",
                "scholarship_type": "merit",
                "degree_level": "UG",
                "field_of_study": "Engineering, Technical Education",
                "eligibility_criteria": "For eligible girl students admitted to approved technical degree programmes. Check the official scheme guidelines for detailed conditions.",
            },
            {
                "title": "AICTE Pragati Scholarship Scheme - Technical Diploma",
                "provider": "AICTE, Government of India",
                "scholarship_type": "merit",
                "degree_level": "HS",
                "field_of_study": "Technical Diploma",
                "eligibility_criteria": "For eligible girl students admitted to approved technical diploma programmes. Check official guidelines.",
            },
            {
                "title": "AICTE Saksham Scholarship Scheme - Technical Degree",
                "provider": "AICTE, Government of India",
                "scholarship_type": "need",
                "degree_level": "UG",
                "field_of_study": "Engineering, Technical Education",
                "eligibility_criteria": "For eligible specially-abled students enrolled in approved technical degree programmes. Check official guidelines.",
            },
            {
                "title": "AICTE Saksham Scholarship Scheme - Technical Diploma",
                "provider": "AICTE, Government of India",
                "scholarship_type": "need",
                "degree_level": "HS",
                "field_of_study": "Technical Diploma",
                "eligibility_criteria": "For eligible specially-abled students enrolled in approved technical diploma programmes. Check official guidelines.",
            },
            {
                "title": "AICTE Swanath Scholarship Scheme - Technical Degree",
                "provider": "AICTE, Government of India",
                "scholarship_type": "need",
                "degree_level": "UG",
                "field_of_study": "Technical Education",
                "eligibility_criteria": "For students meeting the specific Swanath scheme eligibility conditions. Check the official guidelines.",
            },
            {
                "title": "AICTE Swanath Scholarship Scheme - Technical Diploma",
                "provider": "AICTE, Government of India",
                "scholarship_type": "need",
                "degree_level": "HS",
                "field_of_study": "Technical Diploma",
                "eligibility_criteria": "For students meeting the specific Swanath scheme eligibility conditions. Check the official guidelines.",
            },
            {
                "title": "Ishan Uday Special Scholarship Scheme for NER",
                "provider": "UGC, Government of India",
                "scholarship_type": "merit",
                "degree_level": "UG",
                "field_of_study": "All eligible undergraduate fields",
                "eligibility_criteria": "For eligible students from the North Eastern Region pursuing undergraduate studies. Check official guidelines.",
            },
            {
                "title": "National Scholarship for Post Graduate Studies",
                "provider": "UGC, Government of India",
                "scholarship_type": "merit",
                "degree_level": "PG",
                "field_of_study": "Postgraduate Studies",
                "eligibility_criteria": "For eligible postgraduate students meeting the scheme conditions. Check official guidelines.",
            },
            {
                "title": "Top Class Education Scheme for SC Students",
                "provider": "Department of Social Justice and Empowerment",
                "scholarship_type": "need",
                "degree_level": "UG",
                "field_of_study": "Higher Education",
                "category": "SC",
                "eligibility_criteria": "For eligible Scheduled Caste students admitted to notified institutions. Check official guidelines.",
            },
            {
                "title": "Post Matric Scholarship for Students with Disabilities",
                "provider": "Department of Empowerment of Persons with Disabilities",
                "scholarship_type": "need",
                "degree_level": "UG",
                "field_of_study": "All eligible fields",
                "eligibility_criteria": "For eligible students with disabilities pursuing post-matric education. Check official guidelines.",
            },
            {
                "title": "Top Class Education Scholarship for Students with Disabilities",
                "provider": "Department of Empowerment of Persons with Disabilities",
                "scholarship_type": "need",
                "degree_level": "UG",
                "field_of_study": "Higher Education",
                "eligibility_criteria": "For eligible students with disabilities admitted to notified institutions. Check official guidelines.",
            },
            {
                "title": "PM YASASVI Top Class Education in College for OBC, EBC and DNT Students",
                "provider": "Department of Social Justice and Empowerment",
                "scholarship_type": "need",
                "degree_level": "UG",
                "field_of_study": "Higher Education",
                "eligibility_criteria": "For eligible OBC, EBC and DNT students admitted to notified institutions. Check official guidelines.",
            },
        ]

        added = 0
        skipped = 0

        for item in schemes:
            scholarship, created = Scholarship.objects.get_or_create(
                title=item["title"],
                provider=item["provider"],
                defaults={
                    "description": (
                        "Government scholarship scheme listed on the "
                        "National Scholarship Portal for academic year 2026-27. "
                        "Award amount and detailed conditions should be "
                        "confirmed from the official scheme guidelines."
                    ),
                    "scholarship_type": item["scholarship_type"],
                    "amount": 0,
                    "currency": "INR",
                    "number_of_awards": 1,
                    "country": "India",
                    "degree_level": item["degree_level"],
                    "field_of_study": item["field_of_study"],
                    "category": item.get("category", ""),
                    "provider_type": "government",
                    "application_start": date(2026, 6, 1),
                    "deadline": deadline,
                    "eligibility_criteria": item["eligibility_criteria"],
                    "required_documents": "Refer to official scheme guidelines.",
                    "application_url": "https://scholarships.gov.in/All-Scholarships",
                    "status": "active",
                    "is_featured": False,
                    "created_by": None,
                },
            )

            if created:
                added += 1
            else:
                skipped += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Completed! Added: {added}, Already present: {skipped}"
            )
        )
        self.stdout.write(
            f"Total scholarship records: {Scholarship.objects.count()}"
        )
