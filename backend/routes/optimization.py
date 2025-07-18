import sys
import os
import asyncio
import time
from datetime import datetime
from fastapi import APIRouter, Request

router = APIRouter()

# Add OptiRewrite to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from OptiRewrite_optimized import OptiRewriteEngine, RewriteConfig, RewriteMode, RewriteIntensity
    OPTIREWRITE_AVAILABLE = True
    print("✅ OptiRewrite engine loaded successfully")
except ImportError as e:
    OPTIREWRITE_AVAILABLE = False
    print(f"❌ OptiRewrite not available: {e}")

# Global OptiRewrite engine
optirewrite_engine = None

def init_optirewrite():
    """Initialize OptiRewrite engine"""
    global optirewrite_engine
    
    if OPTIREWRITE_AVAILABLE:
        try:
            optirewrite_engine = OptiRewriteEngine()
            print("✅ OptiRewrite engine initialized")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize OptiRewrite: {e}")
            return False
    return False

# Initialize OptiRewrite on module load
init_optirewrite()

@router.post("/api/claudeOptimize")
async def optimize_content(request: Request):
    """Legacy Claude optimization endpoint"""
    prompt = (await request.json()).get("prompt")

    raw_output = await call_claude(prompt)
    optimized_text = format_editorial(raw_output)
    metrics = compute_metrics(prompt, optimized_text)

    return {
        "optimizedText": optimized_text,
        "metrics": metrics,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/api/optimize")
async def optimize_with_optirewrite(request: Request):
    """New OptiRewrite optimization endpoint"""
    
    try:
        data = await request.json()
        
        if not data or 'content' not in data:
            return {
                'success': False,
                'error': 'No content provided'
            }
        
        content = data['content'].strip()
        
        if not content:
            return {
                'success': False,
                'error': 'Empty content provided'
            }
        
        if not optirewrite_engine:
            return {
                'success': False,
                'error': 'OptiRewrite engine not available'
            }
        
        # Get optimization parameters
        mode = data.get('mode', 'engagement')
        intensity = data.get('intensity', 'moderate')
        target_audience = data.get('target_audience', 'general')
        
        # Map string values to enums
        mode_map = {
            'balanced': RewriteMode.BALANCED,
            'clarity': RewriteMode.CLARITY,
            'engagement': RewriteMode.ENGAGEMENT,
            'conciseness': RewriteMode.CONCISENESS,
            'formality': RewriteMode.FORMALITY,
            'creativity': RewriteMode.CREATIVITY,
            'technical': RewriteMode.TECHNICAL,
            'persuasive': RewriteMode.PERSUASIVE,
            'academic': RewriteMode.ACADEMIC,
            'conversational': RewriteMode.CONVERSATIONAL
        }
        
        intensity_map = {
            'light': RewriteIntensity.LIGHT,
            'moderate': RewriteIntensity.MODERATE,
            'heavy': RewriteIntensity.HEAVY,
            'complete': RewriteIntensity.COMPLETE
        }
        
        rewrite_mode = mode_map.get(mode, RewriteMode.ENGAGEMENT)
        rewrite_intensity = intensity_map.get(intensity, RewriteIntensity.MODERATE)
        
        # Create configuration
        config = RewriteConfig(
            mode=rewrite_mode,
            intensity=rewrite_intensity,
            target_audience=target_audience,
            preserve_meaning=True
        )
        
        # Run optimization
        start_time = time.time()
        result = await optirewrite_engine.rewrite(content, config)
        processing_time = time.time() - start_time
        
        # Calculate improvement metrics
        original_length = len(content)
        optimized_length = len(result.rewritten_text)
        length_change = ((optimized_length - original_length) / original_length) * 100
        
        # Calculate estimated value based on improvement
        base_value = max(1.0, len(content) / 100)  # Base value from content length
        confidence_multiplier = result.confidence_score
        strategy_bonus = len(result.strategies_applied) * 0.5
        estimated_value = base_value * confidence_multiplier * (1 + strategy_bonus)
        
        # Quality tier based on confidence
        if result.confidence_score >= 0.8:
            quality_tier = "MASTERY"
        elif result.confidence_score >= 0.6:
            quality_tier = "PROFESSIONAL"
        elif result.confidence_score >= 0.4:
            quality_tier = "COMPETENT"
        else:
            quality_tier = "REMEDIAL"
        
        return {
            'success': True,
            'optimization_id': result.rewrite_id,
            'original_content': content,
            'optimized_content': result.rewritten_text,
            'optimization_summary': {
                'mode': mode,
                'intensity': intensity,
                'strategies_applied': [s.value for s in result.strategies_applied],
                'confidence_score': result.confidence_score,
                'quality_tier': quality_tier,
                'processing_time': processing_time
            },
            'metrics': {
                'original_length': original_length,
                'optimized_length': optimized_length,
                'length_change_percent': round(length_change, 1),
                'word_count_original': len(content.split()),
                'word_count_optimized': len(result.rewritten_text.split()),
                'estimated_value': round(estimated_value, 2)
            },
            'quality_scores': result.quality_scores if hasattr(result, 'quality_scores') else {},
            'recommendations': result.recommendations if hasattr(result, 'recommendations') else [],
            'timestamp': datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        print(f"❌ Optimization error: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            'success': False,
            'error': f'Optimization failed: {str(e)}'
        }

@router.get("/api/sample/{sample_type}")
async def get_sample_content(sample_type: str):
    """Get sample content for testing"""
    
    samples = {
        'blog_post': {
            'title': 'Blog Post Sample',
            'content': """
            Artificial intelligence is changing the world. AI has many applications in different industries. 
            Companies are using AI to improve their processes. This technology offers benefits but also presents challenges.
            Organizations need to consider the implications of AI implementation. The future of AI looks promising.
            """.strip()
        },
        'business_report': {
            'title': 'Business Report Sample',
            'content': """
            Our quarterly analysis shows significant growth in key metrics. Revenue increased by 15% compared to last quarter.
            Customer satisfaction scores improved across all departments. The marketing team exceeded their targets.
            We recommend continuing current strategies while exploring new opportunities for expansion.
            """.strip()
        },
        'educational_content': {
            'title': 'Educational Content Sample',
            'content': """
            Climate change is a global issue that affects everyone. Rising temperatures cause various environmental problems.
            Scientists study weather patterns to understand these changes. Governments and organizations work together to find solutions.
            Individual actions can also make a difference in addressing climate change.
            """.strip()
        },
        'technical_document': {
            'title': 'Technical Document Sample',
            'content': """
            The system architecture consists of multiple components working together. The database stores user information securely.
            API endpoints handle requests from the frontend application. Load balancing ensures optimal performance under high traffic.
            Regular monitoring and maintenance keep the system running smoothly.
            """.strip()
        }
    }
    
    if sample_type not in samples:
        return {
            'success': False,
            'error': 'Invalid sample type'
        }
    
    return {
        'success': True,
        'sample': samples[sample_type]
    }

@router.get("/api/modes")
async def get_optimization_modes():
    """Get available optimization modes"""
    
    modes = {
        'balanced': {
            'name': 'Balanced',
            'description': 'Balance all optimization factors',
            'best_for': 'General content improvement'
        },
        'clarity': {
            'name': 'Clarity',
            'description': 'Focus on clarity and readability',
            'best_for': 'Complex or technical content'
        },
        'engagement': {
            'name': 'Engagement',
            'description': 'Enhance reader engagement',
            'best_for': 'Marketing and blog content'
        },
        'conciseness': {
            'name': 'Conciseness',
            'description': 'Make content more concise',
            'best_for': 'Executive summaries and reports'
        },
        'formality': {
            'name': 'Formality',
            'description': 'Adjust formality level',
            'best_for': 'Business and academic writing'
        },
        'creativity': {
            'name': 'Creativity',
            'description': 'Enhance creative expression',
            'best_for': 'Creative writing and storytelling'
        },
        'technical': {
            'name': 'Technical',
            'description': 'Optimize for technical accuracy',
            'best_for': 'Technical documentation'
        },
        'persuasive': {
            'name': 'Persuasive',
            'description': 'Enhance persuasive power',
            'best_for': 'Sales and marketing content'
        },
        'academic': {
            'name': 'Academic',
            'description': 'Academic writing style',
            'best_for': 'Research papers and essays'
        },
        'conversational': {
            'name': 'Conversational',
            'description': 'Casual, conversational tone',
            'best_for': 'Social media and informal content'
        }
    }
    
    intensities = {
        'light': {
            'name': 'Light',
            'description': 'Minimal changes, preserve original style',
            'change_level': '10-20%'
        },
        'moderate': {
            'name': 'Moderate',
            'description': 'Balanced optimization',
            'change_level': '20-40%'
        },
        'heavy': {
            'name': 'Heavy',
            'description': 'Significant improvements',
            'change_level': '40-60%'
        },
        'complete': {
            'name': 'Complete',
            'description': 'Complete rewrite while preserving meaning',
            'change_level': '60-80%'
        }
    }
    
    return {
        'success': True,
        'modes': modes,
        'intensities': intensities
    }