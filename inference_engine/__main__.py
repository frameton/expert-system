from inference_engine.engine import InferenceEngine

if __name__ == '__main__':
    rules = [
        # [['A', '+', 'B'], '=>', 'D'],
        # [['A', '+', 'B'], '=>', ['C', '+', 'D']],
        # [['A', '+', 'B'], '=>', ['C', '|', ['A', '|', 'D'], '|', ['D', '^', 'C']]],
        [['A', '+', 'B'], '=>', ['C', '^', 'D']],
        ['B', '=>', ['!', 'C']]
    ]
    engine = InferenceEngine(
        rules,
        facts=['A', 'B'],
        goals=['D'],
        # print=True
    )
    engine.infer_goals()

    engine.print_facts()