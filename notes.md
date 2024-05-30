# notes accompanying the coding challenge

## loading the images
There seem to be breaking changes in the PIL versions. Had to revert from 10.... to 9.4.0 to be able to load the images.

## speed up loading:
- multiprocessing
- threads
- async io
I spend a lot of time on this while realizing that those problems might be handled by the api / provider of the data since
we might not have all the files locally. However, here it is the case and a major bottle neck and should be taken care
of to speed up the entire function.

## images
one unit corresponds to two pixels :) - this cost some time since I did not find the correct enterpoint.

## improvements
- convert everything to modules and run as script... maybe then also threading works

## general notes
- should have started earlier to build a complete baseline workflow
- in the initial sketch of the get_image() function, the values are given as floats. Given the description of the
file names, ints were a more intuitive option, which might also be a wrong choice of course

