================
ClassloadGrapher
================

Is your Java program's startup too slow? have you wondered what classes are in your permgen/metaspace and which class was loaded which?
Well then, this tool can help provide some of the answers. It makes a graph of the class loading hierarchy. 


=======
To run:
=======

% java -XX:+TraceClassLoading -XX:+TraceClassUnloading -XX:+TraceClassResolution -jar your-jar.jar > ~/MyClassTraceFile.txt

% python classloadgrapher/clgrapher.py ~/MyClassTraceFile.txt ~/MyClassTraceFile.digraph


And in the same folder you should find a pdf file: ~/MyClassTraceFile.digraph.pdf

A sample screenshot is provided in this repo.

