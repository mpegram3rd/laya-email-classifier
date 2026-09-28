from laya_runner import LayaRunner, ContextTypes

def main():
    runner = LayaRunner()

    # Test direct model access permutations with each model variant using the simple context type
    runner.use_router(False, "convaiinnovations/laya").context_type(ContextTypes.SIMPLE).process()
    runner.use_router(False, "convaiinnovations/laya-multilingual").process()
    runner.use_router(False, "convaiinnovations/laya-typed-decisions").process()

    # Test direct model access permutations with each model variant using the Structured context type
    runner.use_router(False, "convaiinnovations/laya").context_type(ContextTypes.STRUCTURED).process()
    runner.use_router(False, "convaiinnovations/laya-multilingual").process()
    runner.use_router(False, "convaiinnovations/laya-typed-decisions").report_failures(True).process()

if __name__ == "__main__":
    main()
