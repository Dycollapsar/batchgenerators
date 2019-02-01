# Copyright 2017 Division of Medical Image Computing, German Cancer Research Center (DKFZ)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import unittest
import numpy as np
from batchgenerators.augmentations.crop_and_pad_augmentations import random_crop, center_crop, pad_nd_image_and_seg, \
    crop


class TestCrop(unittest.TestCase):

    def setUp(self):
        np.random.seed(1234)

    def test_random_crop_3D(self):
        data = np.random.random((32, 4, 64, 56, 48))
        seg = np.ones(data.shape)

        d, s = random_crop(data, seg, 32, 0)

        self.assertTrue(all(i == j for i, j in zip((32, 4, 32, 32, 32), d.shape)), "data has unexpected return shape")
        self.assertTrue(all(i == j for i, j in zip((32, 4, 32, 32, 32), s.shape)), "seg has unexpected return shape")

        self.assertEqual(np.sum(s == 0), 0, "Zeros encountered in seg meaning that we did padding which should not have"
                                            " happened here!")

    def test_random_crop_2D(self):
        data = np.random.random((32, 4, 64, 56))
        seg = np.ones(data.shape)

        d, s = random_crop(data, seg, 32, 0)

        self.assertTrue(all(i == j for i, j in zip((32, 4, 32, 32), d.shape)), "data has unexpected return shape")
        self.assertTrue(all(i == j for i, j in zip((32, 4, 32, 32), s.shape)), "seg has unexpected return shape")

        self.assertEqual(np.sum(s == 0), 0, "Zeros encountered in seg meaning that we did padding which should not have"
                                            " happened here!")

    def test_random_crop_3D_from_List(self):
        data = [np.random.random((4, 64+i, 56+i, 48+i)) for i in range(32)]
        seg = [np.random.random((4, 64+i, 56+i, 48+i)) for i in range(32)]

        d, s = random_crop(data, seg, 32, 0)

        self.assertTrue(all(i == j for i, j in zip((32, 4, 32, 32), d.shape)), "data has unexpected return shape")
        self.assertTrue(all(i == j for i, j in zip((32, 4, 32, 32), s.shape)), "seg has unexpected return shape")

        self.assertEqual(np.sum(s == 0), 0, "Zeros encountered in seg meaning that we did padding which should not have"
                                            " happened here!")

    def test_random_crop_2D_from_List(self):
        data = [np.random.random((4, 64+i, 56+i)) for i in range(32)]
        seg = [np.random.random((4, 64+i, 56+i)) for i in range(32)]

        d, s = random_crop(data, seg, 32, 0)

        self.assertTrue(all(i == j for i, j in zip((32, 4, 32, 32), d.shape)), "data has unexpected return shape")
        self.assertTrue(all(i == j for i, j in zip((32, 4, 32, 32), s.shape)), "seg has unexpected return shape")

        self.assertEqual(np.sum(s == 0), 0, "Zeros encountered in seg meaning that we did padding which should not have"
                                            " happened here!")

    def test_random_crop_with_cropsize_larger_image(self):
        '''
        should fall back to center crop
        :return:
        '''
        data = [np.random.random((4, 64+i, 56+i)) for i in range(32)]
        seg = [np.random.random((4, 64+i, 56+i)) for i in range(32)]

        d, s = random_crop(data, seg, 32, 32)

        self.assertTrue(all(i == j for i, j in zip((32, 4, 32, 32), d.shape)), "data has unexpected return shape")
        self.assertTrue(all(i == j for i, j in zip((32, 4, 32, 32), s.shape)), "seg has unexpected return shape")

        self.assertEqual(np.sum(s == 0), 0, "Zeros encountered in seg meaning that we did padding which should not have"
                                            " happened here!")

    def test_crop_size_larger_than_image(self):
        data = np.random.random((8, 4, 64, 56))
        seg = np.ones(data.shape)

        d, s = random_crop(data, seg, 96, 0)

        self.assertTrue(all(i == j for i, j in zip((8, 4, 96, 96), d.shape)), "data has unexpected return shape")
        self.assertTrue(all(i == j for i, j in zip((8, 4, 96, 96), s.shape)), "seg has unexpected return shape")

        self.assertNotEqual(np.sum(s == 0), 0, "seg was not padded properly")

    def test_center_crop_3D(self):
        data = np.random.random((8, 4, 30, 30, 30))
        seg = np.random.random(data.shape)
        crop_size = 10

        d, s = center_crop(data, crop_size=crop_size, seg=seg)

        self.assertTrue(all(i == j for i, j in zip((8, 4, crop_size, crop_size, crop_size), d.shape)),
                        "data has unexpected return shape")
        self.assertTrue(all(i == j for i, j in zip((8, 4, crop_size, crop_size, crop_size), s.shape)),
                        "seg has unexpected return shape")

        np.testing.assert_array_equal(data[:, :, 10:20, 10:20, 10:20], d, err_msg="crop not equal image center")
        np.testing.assert_array_equal(seg[:, :, 10:20, 10:20, 10:20], s, err_msg="crop not equal image center")

    def test_center_crop_2D(self):
        data = np.random.random((8, 4, 30, 30))
        seg = np.random.random(data.shape)
        crop_size = 10

        d, s = center_crop(data, crop_size=crop_size, seg=seg)

        self.assertTrue(all(i == j for i, j in zip((8, 4, crop_size, crop_size), d.shape)),
                        "data has unexpected return shape")
        self.assertTrue(all(i == j for i, j in zip((8, 4, crop_size, crop_size), s.shape)),
                        "seg has unexpected return shape")

        np.testing.assert_array_equal(data[:, :, 10:20, 10:20], d, err_msg="crop not equal image center")
        np.testing.assert_array_equal(seg[:, :, 10:20, 10:20], s, err_msg="crop not equal image center")

    def test_center_crop_3D_padding(self):
        data = np.random.random((8, 4, 30, 30, 30))
        seg = np.random.random(data.shape)
        crop_size = 50

        d, s = center_crop(data, crop_size=crop_size, seg=seg)

        self.assertTrue(all(i == j for i, j in zip((8, 4, crop_size, crop_size, crop_size), d.shape)),
                        "data has unexpected return shape")
        self.assertTrue(all(i == j for i, j in zip((8, 4, crop_size, crop_size, crop_size), s.shape)),
                        "seg has unexpected return shape")

        tmp_d = d[:, :, 10:40, 10:40, 10:40]
        tmp_s = s[:, :, 10:40, 10:40, 10:40]
        np.testing.assert_array_equal(tmp_d, data, err_msg="Original data is not included in padded image")
        self.assertAlmostEqual(np.sum(d.flatten()), np.sum(data.flatten()), msg="Padding of data is not zero")

        np.testing.assert_array_equal(tmp_s, seg, err_msg="Original segmentation is not included in padded image")
        self.assertAlmostEqual(np.sum(d.flatten()), np.sum(data.flatten()), msg="Padding of segmentation is not zero")

    def test_center_crop_2D_padding(self):
        data = np.random.random((8, 4, 30, 30))
        seg = np.random.random(data.shape)
        crop_size = 50

        d, s = center_crop(data, crop_size=crop_size, seg=seg)

        self.assertTrue(all(i == j for i, j in zip((8, 4, crop_size, crop_size), d.shape)),
                        "data has unexpected return shape")
        self.assertTrue(all(i == j for i, j in zip((8, 4, crop_size, crop_size), s.shape)),
                        "seg has unexpected return shape")

        tmp_d = d[:, :, 10:40, 10:40]
        tmp_s = s[:, :, 10:40, 10:40]
        np.testing.assert_array_equal(tmp_d, data, err_msg="Original data is not included in padded image")
        self.assertAlmostEqual(np.sum(d.flatten()), np.sum(data.flatten()), msg="Padding of data is not zero")

        np.testing.assert_array_equal(tmp_s, seg, err_msg="Original segmentation is not included in padded image")
        self.assertAlmostEqual(np.sum(d.flatten()), np.sum(data.flatten()), msg="Padding of segmentation is not zero")

    def test_center_crop_2D_list(self):
        data = np.random.random((8, 4, 30, 30))
        seg = np.random.random(data.shape)
        crop_size = [10, 20]

        d, s = center_crop(data, crop_size=crop_size, seg=seg)

        self.assertTrue(all(i == j for i, j in zip((8, 4, crop_size[0], crop_size[1]), d.shape)),
                        "data has unexpected return shape")
        self.assertTrue(all(i == j for i, j in zip((8, 4, crop_size[0], crop_size[1]), s.shape)),
                        "seg has unexpected return shape")

        np.testing.assert_array_equal(data[:, :, 10:20, 5:25], d, err_msg="crop not equal image center")
        np.testing.assert_array_equal(seg[:, :, 10:20, 5:25], s, err_msg="crop not equal image center")

    def test_center_crop_3D_list(self):
        data = np.random.random((8, 4, 30, 30, 30))
        seg = np.random.random(data.shape)
        crop_size = [10, 20, 29]

        d, s = center_crop(data, crop_size=crop_size, seg=seg)

        self.assertTrue(all(i == j for i, j in zip((8, 4, crop_size[0], crop_size[1], crop_size[2]), d.shape)),
                        "data has unexpected return shape")
        self.assertTrue(all(i == j for i, j in zip((8, 4, crop_size[0], crop_size[1], crop_size[2]), s.shape)),
                        "seg has unexpected return shape")

        np.testing.assert_array_equal(data[:, :, 10:20, 5:25, 0:29], d, err_msg="crop not equal image center")
        np.testing.assert_array_equal(seg[:, :, 10:20, 5:25, 0:29], s, err_msg="crop not equal image center")

    def test_pad_nd_image_and_seg_2D(self):
        input_shape = (5, 5, 30, 30)
        data = np.random.random(input_shape)
        seg = np.random.random(data.shape)
        new_shape = (15, 15, 50, 50)
        new_shape2 = (4, 2, 10, 10)

        d, s = pad_nd_image_and_seg(data, seg, new_shape=new_shape)
        d2, s2 = pad_nd_image_and_seg(data, seg, new_shape=new_shape2)

        self.assertTrue(all(i == j for i, j in zip(new_shape, d.shape)), "data has unexpected shape")
        self.assertTrue(all(i == j for i, j in zip(new_shape, s.shape)), "seg has unexpected shape")
        np.testing.assert_array_equal(d[5:10, 5:10, 10:40, 10:40], data, err_msg="data wrongly padded")
        np.testing.assert_array_equal(s[5:10, 5:10, 10:40, 10:40], seg, err_msg="seg wrongly padded")
        self.assertAlmostEqual(np.sum(d.flatten()), np.sum(data.flatten()), msg="Padding of data is not zero")
        self.assertAlmostEqual(np.sum(s.flatten()), np.sum(seg.flatten()), msg="Padding of data is not zero")

        self.assertTrue(all(i == j for i, j in zip(input_shape, d2.shape)), "data has unexpected shape")
        self.assertTrue(all(i == j for i, j in zip(input_shape, s2.shape)), "seg has unexpected shape")
        np.testing.assert_array_equal(d2, data, err_msg="data wrongly padded for smaller output shape than input shape")
        np.testing.assert_array_equal(s2, seg, err_msg="seg wrongly padded for smaller output shape than input shape")

    def test_center_crop_even(self):
        """
        This test will check if center crop really crops the center
        :return:
        """
        data = np.zeros((8, 4, 30, 30, 30))
        seg = np.zeros(data.shape)

        # we set the center that we expect to be cropped to 1 and then check if we only get 1's in the result
        # crop_size is [10, 20, 16] and data_shape is [30, 30, 30]
        crop_size = np.array([10, 20, 16])
        shp = np.array(data.shape[2:])
        border = (shp - crop_size) // 2
        data[:, :, border[0]:(shp[0] + crop_size[0]), border[1]:(shp[1] + crop_size[0]),
        border[2]:(shp[2] + crop_size[0])] = 1
        # same with seg
        seg[:, :, border[0]:(shp[0] + crop_size[0]), border[1]:(shp[1] + crop_size[0]),
        border[2]:(shp[2] + crop_size[0])] = 1

        data_cropped, seg_cropped = crop(data, seg, crop_size, margins=(0, 0, 0), crop_type="center")

        assert np.sum(data_cropped == 0) == 0, "Center crop did not crop the center of data " \
                                               "(even data and crop size)"
        assert np.sum(seg_cropped == 0) == 0, "Center crop did not crop the center of seg (even data and crop size)"

    def test_center_crop_odd(self):
        """
        This test will check if center crop really crops the center
        :return:
        """
        data = np.zeros((8, 4, 30, 30, 30))
        seg = np.zeros(data.shape)

        # we set the center that we expect to be cropped to 1 and then check if we only get 1's in the result
        # crop_size is [10, 20, 16] and data_shape is [30, 30, 30]
        crop_size = np.array([9, 19, 13])
        shp = np.array(data.shape[2:])
        border = (shp - crop_size) // 2
        data[:, :, border[0]:(shp[0] + crop_size[0]), border[1]:(shp[1] + crop_size[0]),
        border[2]:(shp[2] + crop_size[0])] = 1
        # same with seg
        seg[:, :, border[0]:(shp[0] + crop_size[0]), border[1]:(shp[1] + crop_size[0]),
        border[2]:(shp[2] + crop_size[0])] = 1

        data_cropped, seg_cropped = crop(data, seg, crop_size, margins=(0, 0, 0), crop_type="center")

        assert np.sum(data_cropped == 0) == 0, "Center crop did not crop the center of data (even data " \
                                               "and odd crop size)"
        assert np.sum(seg_cropped == 0) == 0, "Center crop did not crop the center of seg (even data and odd crop size)"

    def test_center_crop_negative_margin(self):
        """
        Negative margin means that we are effectively padding if necessary
        :return:
        """
        data = np.ones((8, 4, 30, 30, 30))
        seg = np.ones(data.shape)
        crop_size = np.array([36, 40, 16])
        data_cropped, seg_cropped = center_crop(data, crop_size, seg)

        # data and set are just ones and will be padded of necessary, so the border will be 0
        border = (crop_size - np.array(data.shape[2:])) // 2
        assert np.sum(data_cropped[:, :, 0:border[0]]) == 0
        assert np.sum(data_cropped[:, :, border[0] + crop_size[0]:]) == 0

        assert np.sum(data_cropped[:, :, :, 0:border[1]]) == 0
        assert np.sum(data_cropped[:, :, :, border[1] + crop_size[1]:]) == 0

        data_cropped_back, seg_cropped_back = center_crop(data_cropped, (30, 30, 30), seg_cropped)

        self.assertAlmostEqual(np.sum(data_cropped_back) / np.sum(data), 16 / 30.)

    def test_randomness_1(self):
        data = np.ones((1, 2, 30, 30, 30))
        crop_size = (16, 16, 16)
        margin = (-4, -4, -4)

        sums = [] # these should always be different
        for _ in range(50):
            data_cropped, _ = random_crop(data, crop_size=crop_size, margins=margin)
            s = np.sum(data_cropped[0, 0, 8, 8, :])
            assert 12 <= s <= 16
            sums.append(s)

        assert len(np.unique(sums)) != 0

    def test_randomness_2(self):
        data = np.random.random((1, 1, 30, 30, 30))
        crop_size = (16, 18, 7)
        margin = (-4, -6, 5)

        sums = []  # these should always be different
        for _ in range(50):
            data_cropped, _ = random_crop(data, crop_size=crop_size, margins=margin)
            s = np.sum(data_cropped)
            sums.append(s)

        assert len(np.unique(sums)) == 50


if __name__ == '__main__':
    unittest.main()
