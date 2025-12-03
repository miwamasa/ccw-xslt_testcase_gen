
import subprocess, os, sys
XSLTPROC = "xsltproc"
def transform(xslt, src, out):
    subprocess.run([XSLTPROC, "-o", out, xslt, src])

if __name__ == "__main__":
    mode = "correct"
    if len(sys.argv) > 1 and sys.argv[1] == "--candidate":
        mode = "candidate"
    xslt = "../xslt/T1_candidate.xslt" if mode=="candidate" else "../xslt/T0_correct.xslt"
    input_dir = "../xml/generated_inputs/"
    out_dir = f"../xml/{mode}_outputs/"
    os.makedirs(out_dir, exist_ok=True)
    for f in os.listdir(input_dir):
        transform(xslt, input_dir + f, out_dir + f)
