# ExportHub
Repository of Torch Export Graphs

## Installation

Install the dependencies using pip:

```bash
pip install -r requirements.txt
```

Or install using setup.py:

```bash
pip install -e .
```

## Running the Application

Start the Flask application:

```bash
python run.py
```

The application will be available at `http://localhost:5000`

## Exporting Models

To export all models, run the following:

```bash
python models/export_all.py
```

## Linting

Ruff is used as the main linter. Run the following from the repo root before committing:

```bash
ruff format .
```

## Project Structure

```
export-hub/
├── app/                    # Flask application
│   ├── __init__.py       # App factory
│   ├── routes.py         # Routes and endpoints
│   └── templates/        # HTML templates
│       ├── base.html
│       ├── index.html
│       ├── model_card.html
│       └── 404.html
├── models/               # Model cards directory
│   └── example_model/   # Example model card
│       └── model_card.json
├── setup.py             # Package configuration
├── requirements.txt     # Python dependencies
└── run.py              # Application entry point
```

## Adding Model Cards

To add a new model, create a directory under `models/` with a `model_card.json` file:

```json
{
  "name": "Your Model Name",
  "description": "Model description",
  "model_type": "Torch Export Graph",
  "version": "1.0.0",
  "author": "Your Name",
  "license": "MIT",
  "downloads": [
    {
      "filename": "model.pt",
      "name": "Model File",
      "description": "The exported PyTorch model",
      "size": "10 MB"
    }
  ],
  "technical_details": "Technical details...",
  "usage": "Usage example code..."
}
```

## Features

- Main page listing all available model cards
- Individual model card pages with detailed information
- Download links for model files
- Clean, modern UI
