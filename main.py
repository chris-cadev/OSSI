from fileinput import filename
import os
from factories import ProfileFactory, RelationFactory
from wrappers import PlaywrigthWrapper
import utils


if __name__ == '__main__':
    # only declarative and if statements here
    url = 'https://www.facebook.com/ccamacho.c4'
    profile_factory = ProfileFactory()
    relation_factory = RelationFactory()
    profile_filename = f'{utils.remove_https_protocol(url)}.json'
    if not os.path.exists(os.path.abspath(profile_filename)):
        profile = profile_factory.create_profile_from_url(url)
    else:
        profile = profile_factory.create_profile_from_json(profile_filename)
    profile_dict = profile.__dict__.copy()
    profile_dict['class_name'] = profile.__class__.__name__
    utils.save_object(profile_dict, profile_filename)
    relatives = profile_factory.download_relatives_from_profile(profile)
    print(relatives)
    PlaywrigthWrapper.get_instance().close()
    # relations = relation_factory.generate_relations(profile, relatives)
