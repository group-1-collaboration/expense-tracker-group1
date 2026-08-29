from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from expensetrackerapp.models import Expense
from expensetrackerapp.models import Expense, Category

class ExpenseTests(TestCase):

   def setUp(self):

    self.user = User.objects.create_user(
        username="testuser",
        password="StrongPassword123!"
    )

    self.other_user = User.objects.create_user(
        username="otheruser",
        password="StrongPassword123!"
    )

    self.category = Category.objects.create(
        name="Food"
    )

    self.transport_category = Category.objects.create(
        name="Transport"
    )

   def test_expense_list_requires_login(self):
    response = self.client.get(reverse("expense_list"))

    self.assertEqual(response.status_code, 302)

   def test_logged_in_user_can_view_expenses(self):
    self.client.login(
        username="testuser",
        password="StrongPassword123!"
    )

    response = self.client.get(reverse("expense_list"))

    self.assertEqual(response.status_code, 200)

   def test_expense_list_uses_correct_template(self):
    self.client.login(
        username="testuser",
        password="StrongPassword123!"
    )

    response = self.client.get(reverse("expense_list"))

    self.assertTemplateUsed(response, "expenses/expense_list.html")

   def test_user_can_create_expense(self):
    self.client.login(
        username="testuser",
        password="StrongPassword123!"
    )

    response = self.client.post(
        reverse("add_expense"),
        {
            "amount": 500,
            "category": self.category.id,
            "description": "Lunch"
        }
    )

    self.assertEqual(response.status_code, 302)
    self.assertEqual(Expense.objects.count(), 1)


   def test_expense_category_is_saved(self):

    self.client.login(
        username="testuser",
        password="StrongPassword123!"
    )

    self.client.post(
        reverse("add_expense"),
        {
            "amount": 500,
            "category": self.category.id,
            "description": "Lunch",
            "date": "2026-08-29"
        }
    )

    expense = Expense.objects.first()

    self.assertIsNotNone(expense)

    self.assertEqual(
        expense.category,
        self.category
    )


   def test_expense_belongs_to_logged_in_user(self):

    self.client.login(
        username="testuser",
        password="StrongPassword123!"
    )

    self.client.post(
        reverse("add_expense"),
        {
            "amount": 500,
            "category": self.category.id,
            "description": "Lunch",
            "date": "2026-08-29"
        }
    )

    expense = Expense.objects.first()

    self.assertIsNotNone(expense)

    self.assertEqual(
        expense.user,
        self.user
    )

    response = self.client.get(
        reverse("expense_list")
    )

    expenses = response.context["expenses"]

    self.assertEqual(
        expenses.count(),
        1
    )

    self.assertEqual(
        expenses.first().user,
        self.user
    )


   def test_create_expense_requires_login(self):
    response = self.client.get(reverse("add_expense"))

    self.assertEqual(response.status_code, 302)


   def test_user_can_delete_their_expense(self):
    self.client.login(
        username="testuser",
        password="StrongPassword123!"
    )

    expense = Expense.objects.create(
        user=self.user,
        amount=500,
        category=self.category,
        description="Lunch"
    )

    response = self.client.post(
        reverse("delete_expense", args=[expense.pk])
    )

    self.assertEqual(response.status_code, 302)
    self.assertEqual(Expense.objects.count(), 0)


   def test_expense_list_contains_expense(self):
    Expense.objects.create(
        user=self.user,
        amount=500,
        category=self.category,
        description="Lunch"
    )

    self.client.login(
        username="testuser",
        password="StrongPassword123!"
    )

    response = self.client.get(reverse("expense_list"))

    self.assertContains(response, "Lunch")