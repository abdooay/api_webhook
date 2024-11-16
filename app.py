import datetime
import sys
import os
from flask import Flask, request, jsonify

app = Flask(__name__)


# Helper function to get the correct path when packaged
def resource_path(relative_path):
    """
    Get the correct absolute path for resources when the application is packaged with PyInstaller.

    Args:
        relative_path (str): The relative path to the resource file/directory


    Returns:
        str: The absolute path to the resource
    """
    try:
        base_path = getattr(sys, "_MEIPASS", None)
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def echo_webhook(path):
    response_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "method": request.method,
        "path": f"/{path}",
        "headers": dict(request.headers),
        "query_params": dict(request.args),
        "body": request.get_json(silent=True) or request.form.to_dict() or None,
        "raw_data": request.get_data(as_text=True) or None,
    }

    return jsonify(response_data)


@app.route("/", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def echo_webhook_root():
    return echo_webhook("")


@app.route("/Compquote", methods=["POST"])
def compquote():
    request_data = request.get_json()

    # Initialize response with static values
    response = {
        "value": {
            "status": True,
            "insuranceCompanyCode": 1,
            "maxLiability": 10000000,
            "policyTitleID": 2,
            "vehicleSumInsured": 50000,
            "hasTrailer": False,
            "trailerSumInsure": 0,
            "totalLossPercentage": 0,
            "deductibles": [
                {
                    "deductibleAmount": 0,
                    "policyPremium": 2400.38,
                    "premiumBreakdown": [
                        {
                            "breakdownTypeID": 2,
                            "breakdownPercentage": 0,
                            "breakdownAmount": 1992.36,
                        },
                        {
                            "breakdownTypeID": 14,
                            "breakdownPercentage": 2,
                            "breakdownAmount": 94.93,
                        },
                        {
                            "breakdownTypeID": 20,
                            "breakdownPercentage": 0,
                            "breakdownAmount": 2087.29,
                        },
                        {
                            "breakdownTypeID": 22,
                            "breakdownPercentage": 0,
                            "breakdownAmount": 2400.38,
                        },
                    ],
                    "taxableAmount": 2087.29,
                    "discounts": None,
                    "deductibleReferenceNo": "0",
                }
            ],
            "policyPremiumFeatures": [
                {
                    "featureID": 160,
                    "featureTypeID": 2,
                    "featureAmount": 0,
                    "featureTaxableAmount": 0,
                },
                {
                    "featureID": 161,
                    "featureTypeID": 2,
                    "featureAmount": 0,
                    "featureTaxableAmount": 0,
                },
                {
                    "featureID": 160,
                    "featureTypeID": 2,
                    "featureAmount": 0,
                    "featureTaxableAmount": 0,
                },
                {
                    "featureID": 161,
                    "featureTypeID": 2,
                    "featureAmount": 0,
                    "featureTaxableAmount": 0,
                },
            ],
            "inspectionTypeID": 3,
        },
        "isValid": True,
        "errors": [],
    }

    # Copy matching fields from request to response
    response["value"]["requestReferenceNo"] = request_data.get("RequestReferenceNo")
    response["value"]["quoteReferenceNo"] = request_data.get("RequestReferenceNo")
    response["value"]["policyTitleID"] = request_data.get("PolicyTitleID")
    response["value"]["policyEffectiveDate"] = request_data.get("PolicyEffectiveDate")[
        :10
    ]  # Get only the date part
    response["value"]["policyExpiryDate"] = "2025-11-11"  # Static value for testing
    response["value"]["vehicleSumInsured"] = request_data.get("VehicleSumInsured")
    response["value"]["hasTrailer"] = request_data.get("HasTrailer")
    response["value"]["trailerSumInsure"] = request_data.get("TrailerSumInsured")
    response["value"]["driverDetails"] = [
        {
            "driverID": request_data.get("PolicyHolderID"),
            "driverName": request_data.get("FullName"),
            "vehicleUsagePercentage": 100,
            "driverDateOfBirthG": request_data.get("DateOfBirthG"),
            "driverDateOfBirthH": request_data.get("DateOfBirthH"),
            "driverGender": request_data.get("PolicyholderGender"),
            "ncdEligibility": request_data.get("PolicyHolderNCDEligibility"),
        }
    ]

    return jsonify(response)


def main():
    app.run(debug=False, host="0.0.0.0", port=6000)


if __name__ == "__main__":
    main()
