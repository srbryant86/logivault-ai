@router.post("/api/claudeOptimize")
async def optimize_content(request: Request):
    prompt = (await request.json()).get("prompt")

    raw_output = await call_claude(prompt)
    optimized_text = format_editorial(raw_output)
    metrics = compute_metrics(prompt, optimized_text)

    return {
        "optimizedText": optimized_text,
        "metrics": metrics,
        "timestamp": datetime.utcnow().isoformat(),
    }
