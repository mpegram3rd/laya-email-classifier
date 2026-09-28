from dotenv import load_dotenv

from runners.jev_runner import JevRunner
from runners.laya_runner import LayaRunner
from models import ContextTypes

def main():
    load_dotenv()

    runner = LayaRunner()

    # Test direct model access permutations with each model variant using the simple context type
    runner.use_router(False, "convaiinnovations/laya").context_type(ContextTypes.SIMPLE).process()
    runner.use_router(False, "convaiinnovations/laya-multilingual").process()

    # If you want a shortcut... this is the best performing permutation for Laya from an accuracy standpoint.
    # you can just comment out the other permutations to get a direct head-to-head comparison with Jev.
    runner.use_router(False, "convaiinnovations/laya-typed-decisions").context_type(ContextTypes.SIMPLE).process()

    # Test direct model access permutations with each model variant using the Structured context type
    runner.use_router(False, "convaiinnovations/laya").context_type(ContextTypes.STRUCTURED).process()
    runner.use_router(False, "convaiinnovations/laya-multilingual").process()
    runner.use_router(False, "convaiinnovations/laya-typed-decisions").process()

    # Run scenarios using the router
    runner.use_router(True).context_type(ContextTypes.SIMPLE).process()
    runner.context_type(ContextTypes.STRUCTURED).report_failures(True).process()

    # Run scenarios using Jev (note this will use about 5.8 million tokens costing about $0.24)
    # using the recommended dataset from the README.md
    jev_runner = JevRunner()
    jev_runner.context_type(ContextTypes.SIMPLE).process()

if __name__ == "__main__":
    main()
