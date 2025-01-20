# onavg-template

This repository provides the meshes for the `cortical surface template for human neuroscience` ([PMID: 39014074](https://pubmed.ncbi.nlm.nih.gov/39014074/)) converted to MZ3 format. This allows the meshes to be used with [Surfice](https://www.nitrc.org/plugins/mwiki/index.php/surfice:MainPage#Introduction) and [NiiVue](https://github.com/niivue/niivue). Different [downsamplings](https://brainder.org/tag/freesurfer/) are provided to support specific applications.

NiiVue provides a [live demo web page](https://niivue.github.io/niivue/features/mesh.atlas.onavg.html) to see an example of these mz3 meshes.

In addition to the meshes, [three Cortical Parcellations](https://surfer.nmr.mgh.harvard.edu/fswiki/CorticalParcellation) are included for each decimation level.

For completeness, two Python scripts are also provided that allow the meshes to be reconverted. This is only for advanced users, and is not typically required. To use these, one must clone the [neuroboros core](https://gin.g-node.org/neuroboros/core) repository which retains aliases to the required files. The script `alias2local.py` will download the raw files and save them with a flat naming structure. You must set the `root_folder` to the path of the decimation files you want to convert (e.g. `/Users/chris/core/onavg-ico32` will convert meshes and parcellations for the scale `32`). Once the raw NumPy files are downloaded, you convert them to mz3 format using the script `np2mz3.py` - setting the `order` to the desired scale (e.g. "32"). You may also have to change `root` to be the `root_folder` if the files are not in the current working directory.

More details on the original Python-format meshes can be found at the [neuroboros](https://github.com/neuroboros/neuroboros) repository.