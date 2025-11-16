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
        Searches both by folder name and by JSON organization field.

        Args:
            organization: The organization name (can be from folder or JSON).

        Returns:
            List of model dictionaries matching the organization.
            Uses organization and model_id from JSON if present, otherwise infers from folder/filename.
        """
        models = []
        
        # First, try to find by folder name
        org_dir = self.configs_dir / organization
        if org_dir.exists() and org_dir.is_dir():
            for json_file in org_dir.glob("*.json"):
                try:
                    with open(json_file, "r", encoding="utf-8") as f:
                        model_data = json.load(f)
                        # Use organization from JSON if present, otherwise use folder name
                        if "organization" not in model_data:
                            model_data["organization"] = organization
                        # Use model_id from JSON if present, otherwise use filename
                        if "model_id" not in model_data:
                            model_data["model_id"] = json_file.stem
                        # Store filename for URL routing
                        model_data["_filename_id"] = json_file.stem
                        model_data["config_path"] = str(json_file)
                        models.append(model_data)
                except Exception as e:
                    print(f"Error reading {json_file}: {e}")
        
        # Also search all folders for models with matching JSON organization field
        # (in case organization in JSON doesn't match folder name)
        for org_dir in self.configs_dir.iterdir():
            if not org_dir.is_dir() or org_dir.name == organization:
                continue  # Skip if already processed or not a directory
            
            for json_file in org_dir.glob("*.json"):
                try:
                    with open(json_file, "r", encoding="utf-8") as f:
                        model_data = json.load(f)
                        json_org = model_data.get("organization")
                        if json_org == organization:
                            # Use organization from JSON
                            if "organization" not in model_data:
                                model_data["organization"] = organization
                            # Use model_id from JSON if present, otherwise use filename
                            if "model_id" not in model_data:
                                model_data["model_id"] = json_file.stem
                            # Store filename for URL routing
                            model_data["_filename_id"] = json_file.stem
                            model_data["config_path"] = str(json_file)
                            models.append(model_data)
                except Exception as e:
                    print(f"Error reading {json_file}: {e}")

        return models

    def get_all_models_by_organization(self) -> Dict[str, List[Dict]]:
        """
        Get all models organized by organization.
        Uses organization from JSON if present, otherwise groups by folder.

        Returns:
            Dictionary mapping organization names to lists of model dictionaries.
        """
        if not self.configs_dir.exists():
            return {}

        result = {}
        # Scan all JSON files and group by organization from JSON
        for org_dir in self.configs_dir.iterdir():
            if not org_dir.is_dir():
                continue

            for json_file in org_dir.glob("*.json"):
                try:
                    with open(json_file, "r", encoding="utf-8") as f:
                        model_data = json.load(f)
                        # Use organization from JSON if present, otherwise use folder name
                        org_name = model_data.get("organization", org_dir.name)
                        # Use model_id from JSON if present, otherwise use filename
                        if "model_id" not in model_data:
                            model_data["model_id"] = json_file.stem
                        # Store filename for URL routing
                        model_data["_filename_id"] = json_file.stem
                        model_data["config_path"] = str(json_file)

                        if org_name not in result:
                            result[org_name] = []
                        result[org_name].append(model_data)
                except Exception as e:
                    print(f"Error reading {json_file}: {e}")

        return result

    def get_model(self, organization: str, model_id: str) -> Optional[Dict]:
        """
        Get a specific model by organization and model ID.
        model_id here is the filename without extension (used in URL).

        Args:
            organization: The organization name (folder name).
            model_id: The model ID (JSON filename without extension, used in URL).

        Returns:
            Model dictionary if found, None otherwise.
            Uses organization and model_id from JSON if present.
        """
        json_file = self.configs_dir / organization / f"{model_id}.json"
        if not json_file.exists():
            return None

        try:
            with open(json_file, "r", encoding="utf-8") as f:
                model_data = json.load(f)
                # Use organization from JSON if present, otherwise use parameter
                if "organization" not in model_data:
                    model_data["organization"] = organization
                # Use model_id from JSON if present, otherwise use filename
                if "model_id" not in model_data:
                    model_data["model_id"] = model_id
                # Store filename for URL routing
                model_data["_filename_id"] = model_id
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
