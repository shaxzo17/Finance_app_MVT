from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from django.db import models
from .models import Category, Budget, Transaction
from .serializers import CategorySerializer, BudgetSerializer, TransactionSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def income(self, request):
        qs = self.get_queryset().filter(type="INCOME")
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def expense(self, request):
        qs = self.get_queryset().filter(type="EXPENSE")
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def summary(self, request):
        qs = self.get_queryset()
        income_total = qs.filter(type="INCOME").aggregate(total=Sum('amount'))['total'] or 0
        expense_total = qs.filter(type="EXPENSE").aggregate(total=Sum('amount'))['total'] or 0
        balance = income_total - expense_total

        return Response({
            "income_total": income_total,
            "expense_total": expense_total,
            "balance": balance
        })

    @action(detail=False, methods=['get'])
    def daily_stats(self, request):
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        date = request.query_params.get("date")

        qs = self.get_queryset()

        if date:
            qs = qs.filter(date=date)
            scope = f"{date} kuni"
        elif start_date and end_date:
            qs = qs.filter(date__range=[start_date, end_date])
            scope = f"{start_date} dan {end_date} gacha"
        else:
            serializer = self.get_serializer(qs, many=True)
            return Response({
                "scope": "Umumiy barcha tranzaksiyalar",
                "transactions": serializer.data
            })

        income = qs.filter(type="INCOME").aggregate(total=Sum("amount"))["total"] or 0
        expense = qs.filter(type="EXPENSE").aggregate(total=Sum("amount"))["total"] or 0
        balance = income - expense

        if qs.exists():
            return Response({
                "scope": scope,
                "income": income,
                "expense": expense,
                "balance": balance,
            })
        else:
            return Response({"message": f"{scope} hech qanday tranzaksiya bo‘lmadi"})
