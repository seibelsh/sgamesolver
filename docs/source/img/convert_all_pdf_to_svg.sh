for pdffile in *.pdf; do
    svgfile="$(basename "${pdffile%.pdf}").svg"
    echo "$svgfile";
    eval "pdf2svg $pdffile $svgfile";
done
