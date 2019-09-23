import os
import pdb

import pandas as pd
from torch.utils.data import DataLoader
from torch.utils.data import sampler
from sklearn.model_selection import KFold, StratifiedKFold

from .rsna_dataset import RSNADataset


def provider(df, phase, cfg):
    HOME = cfg.home
    fold = cfg.fold
    total_folds = cfg.total_folds
    kfold = KFold(total_folds, shuffle=True, random_state=69)
    train_idx, val_idx = list(kfold.split(df.filename))[fold]
    train_df, val_df = df.iloc[train_idx], df.iloc[val_idx]
    #any, epidural, intraparenchymal, intraventricular, subarachnoid, subdural
    if 'folder' in cfg.keys():
        # save for analysis, later on
        train_df.to_csv(str(HOME / cfg.folder / f'train{fold}.csv'), index=False)
        val_df.to_csv(str(HOME / cfg.folder / f'val.csv'), index=False)

    df = train_df.copy() if phase == "train" else val_df.copy()

    print(f"{phase}: {df.shape}")

    image_dataset = RSNADataset(df, phase, cfg)
    batch_size = cfg.batch_size[phase]
    num_workers = cfg.num_workers
    dataloader = DataLoader(
        image_dataset,
        batch_size=batch_size,
        num_workers=num_workers,
        pin_memory=True,
        shuffle=True)
    return dataloader


def testprovider(cfg):
    HOME = cfg['home']
    df_path = cfg['sample_submission']
    df = pd.read_csv(os.path.join(HOME, df_path))
    phase = cfg['phase']
    if phase == "test":
        df['id_code'] += '.png'
    batch_size = cfg['batch_size']['test']
    num_workers = cfg['num_workers']


    dataloader = DataLoader(
        ImageDataset(df, phase, cfg),
        batch_size=batch_size,
        num_workers=num_workers,
        pin_memory=True,
        shuffle=False
    )
    return dataloader
