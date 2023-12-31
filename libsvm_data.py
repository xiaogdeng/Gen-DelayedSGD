import os
import numpy as np
from torch.utils.data import DataLoader

import hashlib
import urllib.request
import sklearn.datasets
import torch

CACHE_DIR = os.getenv("LIBSVM_DATASET_DIR", os.path.join(os.getenv("HOME"), "libsvm"))


class LibSVMDataset(torch.utils.data.Dataset):
    def __init__(self, url, data_root=CACHE_DIR, download=False, md5=None, dimensionality=None, classes=None):
        self.url = url
        self.data_root = data_root
        self._dimensionality = dimensionality

        self.filename = os.path.basename(url)
        self.dataset_type = os.path.basename(os.path.dirname(url))

        if not os.path.isfile(self.local_filename):
            if download:
                print(f"Downloading {url}")
                self._download()
                if md5 is not None:  # verify the downloaded file
                    assert self.hash() == md5
            else:
                raise RuntimeError(
                    "Dataset not found or corrupted. You can use download=True to download it."
                )
        elif md5 is not None:
            assert self.hash() == md5
            print("Files already downloaded and verified")
        else:
            print("Files already downloaded")

        is_multilabel = self.dataset_type == "multilabel"
        self.data, y = sklearn.datasets.load_svmlight_file(
            self.local_filename, multilabel=is_multilabel
        )

        sparsity = self.data.nnz / (self.data.shape[0] * self.data.shape[1])
        if sparsity > 0.1:
            self.data = self.data.todense().astype(np.float32)
            self._is_sparse = False
        else:
            self._is_sparse = True

        # convert labels to [0, 1, ...]
        if classes is None:
            classes = np.unique(y)
        self.classes = np.sort(classes)
        self.targets = torch.zeros(len(y), dtype=torch.int64)
        for i, label in enumerate(self.classes):
            self.targets[y == label] = i

        self.class_to_idx = {cl: idx for idx, cl in enumerate(self.classes)}

        super().__init__()

    @property
    def num_classes(self):
        return len(self.classes)

    @property
    def num_features(self):
        return self.data.shape[1]

    def hash(self):
        md5 = hashlib.md5()
        with open(self.local_filename, "rb") as f:
            while True:
                data = f.read(65536)
                if not data:
                    break
                md5.update(data)
        return md5.hexdigest()

    def __getitem__(self, idx):
        if self._is_sparse:
            x = torch.from_numpy(self.data[idx].todense().astype(np.float32)).flatten()
        else:
            x = torch.from_numpy(self.data[idx]).flatten()
        y = self.targets[idx]

        # We may have to pad with zeros
        if self._dimensionality is not None:
            if len(x) < self._dimensionality:
                x = torch.cat([x, torch.zeros([self._dimensionality - len(x)], dtype=x.dtype, device=x.device)])
            elif len(x) > self._dimensionality:
                raise RuntimeError("Dimensionality is set wrong.")

        return x, y

    def __len__(self):
        return len(self.targets)

    @property
    def local_filename(self):
        return os.path.join(self.data_root, self.dataset_type, self.filename)

    def _download(self):
        os.makedirs(os.path.dirname(self.local_filename), exist_ok=True)
        urllib.request.urlretrieve(self.url, filename=self.local_filename)


class IJCNN1(LibSVMDataset):
    def __init__(self, split, download=False, data_root=CACHE_DIR):
        if split == "train":
            url = "https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary/ijcnn1.tr.bz2"
            md5 = "9889c2e9d957dca5304ed2d285f1be6d"
        elif split == "test":
            url = "https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary/ijcnn1.t.bz2"
            md5 = "66433ab8089acee9e56dc61ac89a2fe2"
        elif split == "val":
            url = "https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary/ijcnn1.val.bz2"
            md5 = "9940e6f83e00623a5ca993f189ab18d9"
        else:
            raise RuntimeError(f"Unavailable split {split}")
        super().__init__(url=url, md5=md5, download=download, data_root=data_root)


class CovTypeBinary(LibSVMDataset):
    def __init__(self, download=False, scale=True, data_root=CACHE_DIR):
        if scale:
            url = "https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary/covtype.libsvm.binary.scale.bz2"
            md5 = "d95f45e15c284005c2c7a4c82e4be102"
        else:
            url = "https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary/covtype.libsvm.binary.bz2"
            md5 = "0d3439b314ce13e2f8b903b12bb3ea20"
        super().__init__(url=url, md5=md5, download=download, data_root=data_root)


class RCV1MultiClass(LibSVMDataset):
    def __init__(self, split, download=False, data_root=CACHE_DIR):
        if split == "train":
            url = "https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/multiclass/rcv1_train.multiclass.bz2"
            md5 = "b0ce08cd1a4c9e15c887c20acfb0eade"
        elif split == "test":
            url = "https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/multiclass/rcv1_test.multiclass.bz2"
            md5 = "68a377cfff6f4a82edac1975b148afd3"
        else:
            raise RuntimeError(f"Unavailable split {split}")
        super().__init__(url=url, md5=md5, download=download, data_root=data_root, classes=np.arange(53))


class RCV1Binary(LibSVMDataset):
    def __init__(self, split, download=False, data_root=CACHE_DIR):
        if split == "train":
            url = "https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary/rcv1_train.binary.bz2"
            md5 = "1aeda848408e621468c0fe6944d9382f"
        elif split == "test":
            url = "https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary/rcv1_test.binary.bz2"
            md5 = "d6e3ab397758fb5c036d9cced52aedae"
        else:
            raise RuntimeError(f"Unavailable split {split}")
        super().__init__(url=url, md5=md5, download=download, data_root=data_root)


class GISETTE(LibSVMDataset):
    def __init__(self, split, download=False, data_root=CACHE_DIR):
        if split == "train":
            url = "https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary/gisette_scale.bz2"
            md5 = "8a8caa1628c98dafec8d5d7bfa67c20b"
        elif split == "test":
            url = "https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary/gisette_scale.t.bz2"
            md5 = "28033576433100e2db6154920737232b"
        else:
            raise RuntimeError(f"Unavailable split {split}")
        super().__init__(url=url, md5=md5, download=download, data_root=data_root)
