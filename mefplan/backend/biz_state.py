import reflex as rx
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from typing import List, Optional, Literal

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

IndustryEnum = Literal[
    "Building & Construction Services",
    "Financial & Wealth Management",
    "Legal Services",
    "Food & Drink",
    "Information Technology",
    "Art",
    "Business Services",
    "Youth Programs",
    "Photography",
    "Financial Services",
    "Travel & Tourism",
    "Supportive Services",
    "Other",
    "Consumer Services",
    "Women's Empowerment",
    "Insurance",
    "Faith-Based",
    "Community Resources & Supportive Services",
    "Human Resources",
    "Housing",
    "Quality Education",
]


class Business(rx.Base):
    company_name: str
    website: Optional[str] = None
    industry: IndustryEnum


class BizState(rx.State):
    businesses: List[Business] = []
    page_number: int = 1
    items_per_page: int = 25
    search_value: str = ""
    sort_value: str = ""
    sort_reverse: bool = False
    new_company_name: str = ""
    new_website: str = ""
    new_industry: IndustryEnum = "Other"

    def get_business_info(self):
        try:
            response = (
                supabase.table("COAACC Businesses")
                .select("company_name,website,industry")
                .execute()
            )
            if response.data:
                self.businesses = [Business(**item) for item in response.data]
            else:
                print("No data found in the table.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def add_business_to_db(self, form_data: dict):
        new_business = Business(
            company_name=form_data["company_name"],
            website=form_data["website"],
            industry=form_data["industry"],
        )
        try:
            response = (
                supabase.table("COAACC Businesses")
                .insert(new_business.dict())
                .execute()
            )
            if response.data:
                self.businesses.append(new_business)
                self.new_company_name = ""
                self.new_website = ""
                self.new_industry = "Other"
            else:
                print("Failed to add new business.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    @rx.var
    def total_pages(self) -> int:
        return max(
            1,
            (len(self.filtered_businesses) + self.items_per_page - 1)
            // self.items_per_page,
        )

    @rx.var
    def filtered_businesses(self) -> List[Business]:
        if not self.search_value:
            return self.businesses
        return [
            b
            for b in self.businesses
            if self.search_value.lower() in b.company_name.lower()
        ]

    @rx.var
    def sorted_businesses(self) -> List[Business]:
        if not self.sort_value:
            return self.filtered_businesses
        return sorted(
            self.filtered_businesses,
            key=lambda b: getattr(b, self.sort_value),
            reverse=self.sort_reverse,
        )

    @rx.var
    def current_page_businesses(self) -> List[Business]:
        start = (self.page_number - 1) * self.items_per_page
        end = start + self.items_per_page
        return self.sorted_businesses[start:end]

    @rx.var
    def total_businesses(self) -> int:
        return len(self.businesses)

    @rx.var
    def total_industries(self) -> int:
        return len(set(b.industry for b in self.businesses))

    @rx.var
    def businesses_with_website(self) -> int:
        return sum(1 for b in self.businesses if b.website)

    def next_page(self):
        if self.page_number < self.total_pages:
            self.page_number += 1

    def prev_page(self):
        if self.page_number > 1:
            self.page_number -= 1

    def first_page(self):
        self.page_number = 1

    def last_page(self):
        self.page_number = self.total_pages

    def set_search_value(self, value: str):
        self.search_value = value
        self.page_number = 1

    def set_sort_value(self, value: str):
        if self.sort_value == value:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_value = value
            self.sort_reverse = False
        self.page_number = 1

    def toggle_sort(self):
        self.sort_reverse = not self.sort_reverse
