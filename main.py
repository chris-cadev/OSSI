from profiles import ProfileFactory
from relationships import RelationFactory


if __name__ == '__main__':
    # only declarative and if statements here
    url = 'https://www.facebook.com/ccamacho.c4'
    profile_factory = ProfileFactory()
    relation_factory = RelationFactory()
    profile = profile_factory.create_profile(url)
    print(profile.__dict__)
    # relatives = profile_factory.download_relatives_from_profile(profile)
    # relations = relation_factory.generate_relations(profile, relatives)
