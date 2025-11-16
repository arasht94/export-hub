from flask import Blueprint, render_template
from app.config_parser import ConfigParser

main = Blueprint("main", __name__)

# Initialize the config parser
parser = ConfigParser()


@main.route("/")
def index():
    """Main page showing organizations with top models in 2x3 grids"""
    organizations_data = parser.get_all_models_by_organization()
    # Get top 6 models for each organization
    orgs_with_models = {}
    for org, models in organizations_data.items():
        orgs_with_models[org] = models[:6]  # Just take first 6 from the list

    return render_template("index.html", organizations=orgs_with_models)


@main.route("/organization/<organization>")
def organization_page(organization):
    """Organization page showing all models for an organization"""
    models = parser.get_models_by_organization(organization)

    if not models:
        return render_template(
            "404.html",
            message=f"Organization '{organization}' not found or has no models",
        ), 404

    return render_template(
        "organization.html", organization=organization, models=models
    )


@main.route("/model/<organization>/<model_id>")
def model_page(organization, model_id):
    """Individual model card page"""
    model_card = parser.get_model(organization, model_id)

    if not model_card:
        return render_template(
            "404.html",
            message=f"Model card '{model_id}' in organization '{organization}' not found",
        ), 404

    return render_template("model_card.html", card=model_card)


# Download route - kept for future use if model files are stored
# @main.route("/download/<organization>/<model_id>/<filename>")
# def download_file(organization, model_id, filename):
#     """Download endpoint for model files"""
#     # Implementation would depend on where model files are stored
#     return jsonify({"error": "Not implemented"}), 404
