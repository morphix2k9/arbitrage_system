import os
import zipfile
from pathlib import Path

def create_project_structure():
    """Create the project structure and write scripts to files."""
    project_name = "arbitrage_system"
    project_path = Path(project_name)
    if project_path.exists():
        for item in project_path.glob("**/*"):
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                item.rmdir()
    
    project_path.mkdir()

    # Directory structure
    directories = [
        "app", "app/routers", "app/models", "app/utils", "config", "src", "src/utils",
        "tests", "docs"
    ]
    for directory in directories:
        (project_path / directory).mkdir(parents=True)

    # Script content (as provided in previous responses)
    scripts = {
        "requirements.txt": """
        fastapi==0.109.0
        uvicorn==0.25.0
        requests==2.31.0
        pandas==2.2.0
        numpy==1.26.0
        google-api-python-client==2.108.0
        facebook-business==18.0.0
        twilio==8.10.0
        python-dotenv==1.0.0
        """,
        ".gitignore": "venv/\n__pycache__/\n*.pyc\n*.pyo\n*.pyd\n.Python\nenv/\n.env\nnode_modules/\n.vercel/\n",
        "README.md": "# Arbitrage System\nAn AI-driven automated arbitrage system using FastAPI, Python, and Vercel.\n\n## Setup\n1. Run `python setup_project.py`\n2. Open in VS Code and install extensions.\n3. Deploy to Vercel using `vercel deploy`.",
        "setup_project.py": open(__file__, "r").read().replace("setup_project.py", "setup_project.py"),
        "main.py": '# Entry point for the system\nprint("Arbitrage system setup complete!")',
        "app/main.py": '''from fastapi import FastAPI
from app.routers import product_discovery, price_comparison, seller_outreach, purchase_automation, resale_listings

app = FastAPI(title="Arbitrage System API")

# Include routers
app.include_router(product_discovery.router)
app.include_router(price_comparison.router)
app.include_router(seller_outreach.router)
app.include_router(purchase_automation.router)
app.include_router(resale_listings.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Arbitrage System API"}''',
        "app/routers/product_discovery.py": '''from fastapi import APIRoute

router = APIRouter(prefix="/products", tags=["product_discovery"])

@router.get("/discover")
async def discover_products():
    return {"message": "Discovering trending products..."}''',
        "app/routers/price_comparison.py": '''from fastapi import APIRouter

router = APIRouter(prefix="/prices", tags=["price_comparison"])

@router.get("/compare")
async def compare_prices():
    return {"message": "Comparing prices for profit margins..."}''',
        "app/routers/seller_outreach.py": '''from fastapi import APIRouter

router = APIRouter(prefix="/sellers", tags=["seller_outreach"])

@router.post("/negotiate")
async def negotiate_sellers():
    return {"message": "Negotiating with sellers..."}''',
        "app/routers/purchase_automation.py": '''from fastapi import APIRouter

router = APIRouter(prefix="/purchases", tags=["purchase_automation"])

@router.post("/automate")
async def automate_purchases():
    return {"message": "Automating purchases..."}''',
        "app/routers/resale_listings.py": '''from fastapi import APIRouter

router = APIRouter(prefix="/listings", tags=["resale_listings"])

@router.post("/list")
async def list_products():
    return {"message": "Listing products for resale..."}''',
        "config/config.py": '''import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_TRENDS_API_KEY = os.getenv("GOOGLE_TRENDS_API_KEY")
    FACEBOOK_API_KEY = os.getenv("FACEBOOK_API_KEY")
    AMAZON_API_KEY = os.getenv("AMAZON_API_KEY")
    EBAY_API_KEY = os.getenv("EBAY_API_KEY")
    STOCKX_API_KEY = os.getenv("STOCKX_API_KEY")
    ZELLE_API_KEY = os.getenv("ZELLE_API_KEY")
    MIN_PROFIT_MARGIN = 0.28''',
        "vercel.json": '''{
    "version": 2,
    "builds": [
        {
            "src": "app/main.py",
            "use": "@vercel/python"
        }
    ],
    "routes": [
        {
            "src": "/(.*)",
            "dest": "app/main.py"
        }
    ]
}'''
    }

    # Write scripts to files
    for file_name, content in scripts.items():
        with open(project_path / file_name, "w") as f:
            f.write(content)

def create_zip_file(project_path, zip_name="arbitrage_system.zip"):
    """Create a ZIP file containing the project."""
    zip_path = Path(zip_name)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(project_path):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(project_path)
                zipf.write(file_path, arcname)
    print(f"ZIP file created: {zip_path}")

def main():
    """Main function to set up and zip the project."""
    project_name = "arbitrage_system"
    create_project_structure()
    project_path = Path(project_name)
    create_zip_file(project_path)
    print(f"Download {project_name}.zip and extract it to use in VS Code.")

if __name__ == "__main__":
    main()