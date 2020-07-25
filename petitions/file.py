import pdfcrowd
import sys

try:
    # create the API client instance
    client = pdfcrowd.HtmlToImageClient('Regards', 'a4ba1c683a712b98f7475abcbabb10e5')

    # configure the conversion
    client.setOutputFormat('png')

    # create output file for conversion result
    output_file = open('example.png', 'wb')

    # run the conversion and store the result into an image variable
    image = client.convertFileToFile('/home/vitalikz/Desktop/timetable.html', 'zz.png')

    # write the image the into the output file

    output_file.write(image)

    # close the output file
    output_file.close()
except pdfcrowd.Error as why:
    # report the error to the standard error stream
    sys.stderr.write('Pdfcrowd Error: {}\n'.format(why))