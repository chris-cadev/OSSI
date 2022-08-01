class RelationFactory:
    def generate_relation(self, parent, child):
        return {
            "source": f'{parent}',
            "target": f'{child}'
        }

    def generate_relations(self, parent, children):
        relations = []
        for child in children:
            relation = self.generate_relation(parent, child)
            relations.append(relation)

        return relations
