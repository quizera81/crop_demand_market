from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Crop, Transaction
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
        print(self.df)

    def computations(self):
        self.df["Total_Produced_Price"] = (
            self.df["KG Sold"] * self.df["Production Price"]
        )
        self.df["Total_Selling_Price"] = self.df["KG Sold"] * self.df["Selling Price"]

        self.df["Unsold KG"] = self.df["KG received"] - self.df["KG Sold"]
        self.df["Profit made"] = (
            self.df["Total_Selling_Price"] - self.df["Total_Produced_Price"]
        )
        print(self.df)

    def recomended_crop(self):
        trial = self.df
        row_index = trial.loc[
            trial["Unsold KG"] == (trial.groupby("Crops")["Unsold KG"].min()).min()
        ]["Profit made"].idxmax()

        print(
            "The recommended crop based on stock demand and profitability is : "
            + self.crops[row_index]
        )


# test = RecommendedSystem()
# test.dataframe()
# test.computations()
# test.recomended_crop()


@login_required(login_url="signin")
def analytics(request):
    if request.method == "GET":
        return render(request, "analytics.html")

    elif request.method == "POST":
        end = request.POST["end"]
        start = request.POST["start"]
