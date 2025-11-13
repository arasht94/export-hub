"""Parser class for reading and organizing model configs from the configs folder."""
import os
import json
from pathlib import Path
from typing import Dict, List, Optional


class ConfigParser:
    """Parses the configs folder structure and model card JSON files."""

    def __init__(self, configs_dir: Optional[str] = None):
        """
        Initialize the parser with the configs directory path.

        Args:
            configs_dir: Path to the configs directory. If None, uses default location.
        """
        if configs_dir is None:
            # Default to models/configs relative to the app directory
            base_dir = os.path.dirname(os.path.dirname(__file__))
            configs_dir = os.path.join(base_dir, "models", "configs")
        self.configs_dir = Path(configs_dir)

    def get_organizations(self) -> List[str]:
        """
        Get list of all organization names (first-level subfolders).

        Returns:
            List of organization names, sorted alphabetically.
        """
        if not self.configs_dir.exists():
            return []

        organizations = []
        for item in self.configs_dir.iterdir():
            if item.is_dir():
                organizations.append(item.name)

        return sorted(organizations)

    def get_models_by_organization(self, organization: str) -> List[Dict]:
        """
        Get all models for a specific organization.

        Args:
            organization: The organization name (subfolder name).

        Returns:
            List of model dictionaries, each containing the parsed JSON data
            plus metadata like 'model_id' and 'organization'.
        """
        org_dir = self.configs_dir / organization
        if not org_dir.exists() or not org_dir.is_dir():
            return []

        models = []
        for json_file in org_dir.glob("*.json"):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    model_data = json.load(f)
                    # Add metadata
                    model_data["model_id"] = json_file.stem  # filename without .json
                    model_data["organization"] = organization
                    model_data["config_path"] = str(json_file)
                    models.append(model_data)
            except Exception as e:
                print(f"Error reading {json_file}: {e}")

        return models

    def get_all_models_by_organization(self) -> Dict[str, List[Dict]]:
        """
        Get all models organized by organization.

        Returns:
            Dictionary mapping organization names to lists of model dictionaries.
        """
        organizations = self.get_organizations()
        result = {}

        for org in organizations:
            models = self.get_models_by_organization(org)
            result[org] = models

        return result

    def get_model(self, organization: str, model_id: str) -> Optional[Dict]:
        """
        Get a specific model by organization and model ID.

        Args:
            organization: The organization name.
            model_id: The model ID (JSON filename without extension).

        Returns:
            Model dictionary if found, None otherwise.
        """
        json_file = self.configs_dir / organization / f"{model_id}.json"
        if not json_file.exists():
            return None

        try:
            with open(json_file, "r", encoding="utf-8") as f:
                model_data = json.load(f)
                model_data["model_id"] = model_id
                model_data["organization"] = organization
                model_data["config_path"] = str(json_file)
                return model_data
        except Exception as e:
            print(f"Error reading {json_file}: {e}")
            return None

    def get_top_models(self, organization: str, limit: int = 6) -> List[Dict]:
        """
        Get top N models for an organization (currently just returns first N).

        Args:
            organization: The organization name.
            limit: Maximum number of models to return (default: 6 for 2x3 grid).

        Returns:
            List of model dictionaries, limited to top N.
        """
        models = self.get_models_by_organization(organization)
        return models[:limit]

