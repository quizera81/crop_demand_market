from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Crop, Transaction
from django.http import HttpResponse
import pandas as pd
import numpy as np


class RecommendedSystem:
    def __init__(self):
        self.crops = []
        self.kgs_sold = []
        self.kgs_received = []
        self.selling_price_per_kg = []
        self.production_cost_per_kg = []

    def dataframe(self):
        data = {
            "Crops": self.crops,
            "KG received": self.kgs_received,
            "KG Sold": self.kgs_sold,
            "Production Price": self.production_cost_per_kg,
            "Selling Price": self.selling_price_per_kg,
        }

        self.df = pd.DataFrame(data)

    def computations(self):
        self.df["Total_Produced_Price"] = (
            self.df["KG Sold"] * self.df["Production Price"]
        )
        self.df["Total_Selling_Price"] = self.df["KG Sold"] * self.df["Selling Price"]

        self.df["Unsold KG"] = self.df["KG received"] - self.df["KG Sold"]
        self.df["Profit made"] = (
            self.df["Total_Selling_Price"] - self.df["Total_Produced_Price"]
        )

    def recommended_crop(self):
        trial = self.df
        row_index = trial.loc[
            trial["Unsold KG"] == (trial.groupby("Crops")["Unsold KG"].min()).min()
        ]["Profit made"].idxmax()

        return self.crops[row_index]


@login_required(login_url="signin")
def analytics(request):
    if request.method == "GET":
        return render(request, "analytics.html")

    elif request.method == "POST":
        end = request.POST["end"]
        start = request.POST["start"]
        analysis = RecommendedSystem()

        for crop in Crop.objects.all().distinct("name"):
            analysis.crops.append(crop["name"])
            analysis.selling_price_per_kg.append(crop["selling_price"])
            analysis.production_cost_per_kg.append(crop["production_cost"])

        for transaction in Transaction.objects.all().distinct("crop_id"):
            analysis.kgs_sold.append()
            analysis.kgs_received.append()

        analysis.dataframe()
        analysis.computations()
        return HttpResponse(analysis.recommended_crop())
