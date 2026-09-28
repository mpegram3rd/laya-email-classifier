from laya_runner import LayaRunner
from models import ContextTypes

def main():
    runner = LayaRunner()

    # Test direct model access permutations with each model variant using the simple context type
    runner.use_router(False, "convaiinnovations/laya").context_type(ContextTypes.SIMPLE).process()
    runner.use_router(False, "convaiinnovations/laya-multilingual").process()
    runner.use_router(False, "convaiinnovations/laya-typed-decisions").process()

    # Test direct model access permutations with each model variant using the Structured context type
    runner.use_router(False, "convaiinnovations/laya").context_type(ContextTypes.STRUCTURED).process()
    runner.use_router(False, "convaiinnovations/laya-multilingual").process()
    runner.use_router(False, "convaiinnovations/laya-typed-decisions").process()

    # Run scenarios using the router
    runner.use_router(True).context_type(ContextTypes.SIMPLE).process()
    runner.context_type(ContextTypes.STRUCTURED).report_failures(True).process()

    # Run scenarios using Jev
    jev_runner = JevRunner()
    jev_runner.process()

if __name__ == "__main__":
    main()
