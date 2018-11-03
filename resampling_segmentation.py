from __future__ import division
import os
import sys
import argparse
import nibabel as nib
import numpy as np
import dipy
from dipy.tracking.utils import length
from dipy.tracking.streamline import set_number_of_points


def resample_tract(tract, step_size):
    """Resample the tract with the given step size.
    """
    lengths=list(length(tract))
    tract_res = []
    for i, f in enumerate(tract):
	nb_res_points = np.int(np.floor(lengths[i]/step_size))
	tmp = set_number_of_points(f, nb_res_points)
	tract_res.append(tmp)
    tract_res = nib.streamlines.array_sequence.ArraySequence(tract_res)
    return tract_res


def save_tract(tract, t1_filename, out_filename):
	"""Save the tract in trk or tck format.
	"""
	extension = os.path.splitext(out_filename)[1]
	t1 = nib.load(t1_filename)
	aff_vox_to_ras = t1.affine
	header = t1.header
	dimensions = header.get_data_shape()
	voxel_sizes = header.get_zooms()
	
	if extension == '.trk':
		hdr = nib.streamlines.trk.TrkFile.create_empty_header()
		hdr['voxel_sizes'] = voxel_sizes
		hdr['dimensions'] = dimensions
		hdr['voxel_order'] = 'LAS'
		hdr['voxel_to_rasmm'] = aff_vox_to_ras 
	elif extension == '.tck':
		hdr = nib.streamlines.tck.TckFile.create_empty_header()
		hdr['voxel_sizes'] = voxel_sizes
		hdr['dimensions'] = dimensions
	else:
		print("%s format not supported." % extension)

	t = nib.streamlines.tractogram.Tractogram(tract, affine_to_rasmm=np.eye(4))
	nib.streamlines.save(t, out_filename, header=hdr)
	print("Bundle saved in %s" % out_filename)


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-trk_dir', nargs='?', const=1, default='',
	                    help='Directory of the trk files')   
	parser.add_argument('-t1', nargs='?', const=1, default='',
	                    help='T1 filename')  
	parser.add_argument('-step_size', nargs='?', const=1, default='',
	                    help='The step size to use for resampling (in mm)')    
	parser.add_argument('-out_dir', nargs='?', const=1, default='',
	                    help='The output directory')                                           
	args = parser.parse_args()

	tracts = os.listdir(args.trk_dir)
	step_size = np.asarray(args.step_size, dtype='float64')

	for i in range(len(tracts)):
		tract = '%s/%s' %(args.trk_dir, tracts[i])
		tract = nib.streamlines.load(tract).streamlines
		tract_res = resample_tract(tract, step_size)
		out_filename = '%s/%s' %(args.out_dir, tracts[i])
		save_tract(tract_res, t1, out_filename)

	sys.exit()
