from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.bundle import Bundle, BundleResponse
from app.database import get_db
import json

router = APIRouter()

# Preset bundles data
PRESET_BUNDLES = [
    {
        "id": "preset-1",
        "key": "ai-ml-trends",
        "label": "AI & ML Trends",
        "description": "The latest news, research, and breakthroughs in Artificial Intelligence and Machine Learning.",
        "is_preset": True,
        "sources": [
            "https://techcrunch.com/category/artificial-intelligence/feed/",
            "https://venturebeat.com/category/ai/feed/",
        ],
    },
    {
        "id": "preset-2",
        "key": "creator-economy",
        "label": "Creator Economy",
        "description": "Insights on the creator economy, monetization, and platform trends.",
        "is_preset": True,
        "sources": [],
    },
    {
        "id": "preset-3",
        "key": "marketing-growth",
        "label": "Marketing & Growth",
        "description": "Growth hacking, marketing strategies, and conversion optimization.",
        "is_preset": True,
        "sources": [],
    },
    {
        "id": "preset-4",
        "key": "startups-innovation",
        "label": "Startups & Innovation",
        "description": "Startup news, funding rounds, and innovation in tech.",
        "is_preset": True,
        "sources": [],
    },
    {
        "id": "preset-5",
        "key": "cybersecurity-privacy",
        "label": "Cybersecurity & Privacy",
        "description": "Security vulnerabilities, privacy concerns, and data protection news.",
        "is_preset": True,
        "sources": [],
    },
    {
        "id": "preset-6",
        "key": "productivity-workflow",
        "label": "Productivity & Workflow Tools",
        "description": "Tools and techniques to boost productivity and streamline workflows.",
        "is_preset": True,
        "sources": [],
    },
    {
        "id": "preset-7",
        "key": "sustainability-future-tech",
        "label": "Sustainability & Future Tech",
        "description": "Green technology, climate tech, and sustainable innovation.",
        "is_preset": True,
        "sources": [],
    },
    {
        "id": "preset-8",
        "key": "tech-policy-regulation",
        "label": "Tech Policy & Regulation",
        "description": "Regulatory changes, policy debates, and legal issues in tech.",
        "is_preset": True,
        "sources": [],
    },
    {
        "id": "preset-9",
        "key": "health-wellness-tech",
        "label": "Health & Wellness Tech",
        "description": "Digital health, wellness apps, and medical technology.",
        "is_preset": True,
        "sources": [],
    },
    {
        "id": "preset-10",
        "key": "mindset-creativity",
        "label": "Mindset & Creativity",
        "description": "Creative thinking, mental models, and personal development.",
        "is_preset": True,
        "sources": [],
    },
]


@router.get("/presets", response_model=List[BundleResponse])
async def get_preset_bundles():
    """Get all preset bundles"""
    return PRESET_BUNDLES


@router.get("/", response_model=List[BundleResponse])
async def get_all_bundles(user_id: str = None):
    """Get all bundles (presets + user custom bundles)"""
    # For MVP, just return presets
    # TODO: Add user custom bundles from database
    return PRESET_BUNDLES


@router.get("/{bundle_id}", response_model=BundleResponse)
async def get_bundle(bundle_id: str):
    """Get a specific bundle by ID"""
    bundle = next((b for b in PRESET_BUNDLES if b["id"] == bundle_id), None)
    if not bundle:
        raise HTTPException(status_code=404, detail="Bundle not found")
    return bundle

