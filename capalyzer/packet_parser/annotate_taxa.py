
import pandas as pd
from .taxa_tree import NCBITaxaTree
from ..constants import MICROBE_DIR

MICROBE_DIR_COLS = [
    'gram_stain',
    'microbiome_location',
    'antimicrobial_susceptibility',
    'optimal_temperature',
    'extreme_environment',
    'biofilm_forming',
    'optimal_ph',
    'animal_pathogen',
    'spore_forming',
    'pathogenicity',
    'plant_pathogen'
]


def annotate_taxa(taxa):
    """Return a pandas dataframe with annotations for the given taxa."""
    taxa_tree = NCBITaxaTree.parse_files()
    phyla = [taxa_tree.phyla(taxon, 'unknown') for taxon in taxa]
    annotated = pd.DataFrame.from_dict({'taxa': taxa, 'phyla': phyla}, orient='columns')
    annotated = annotated.set_index('taxa')

    microbe_dir = pd.read_csv(MICROBE_DIR).set_index('species')
    annotated = annotated.join(microbe_dir[MICROBE_DIR_COLS], how='left')
    return annotated
