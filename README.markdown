Inkling represents a series of attempts to create an effective note-taking app for a tablet computer. Existing programs all attempt to mimic writing on paper which defies the whole point of using a tablet. Inkling revolved around a three basic ideas:

* Notetaking is not linear. Notes should be short, separate, tagged and hyperlinked.
* Handwriting should not be converted to print. Handwriting recognition should instead be used to populate search indices.
* We are not going to run out of paper. The writing area should not be limited in size.

Inkling's (gnote) was a short prototype using haskell and cairo/gtk. 

The second implementation (jottinks) used python and qt. This version suffered from an overabundance of inheritance and mutable state. Unfortunately this is difficult to avoid when using pyqt.

The third implementation (inkling) used clojure and qt. This ran afoul of the unreasonable level of introspection used in QtJava. For example, Qt slots are found by scanning the fields of their parent class. This means that a slot will fail silently if it is not a concretely typed field of a Java class. QtJava does not play well with clojure.

Inkling is not truly dead, just resting.
