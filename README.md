Queryset Iterator ReadMe
========================

General
-------

Queryset Iterator is a tool that is useful for iterating over large datasets
in Django.

Queryset Iterator iterates over large datasets in batches, which can be
manually set to any batch size of your choosing, to improve performance.
The iterator maintains an open database cursor to a median table containing
only the primary keys of the results that would normally be obtained. Due to
this, primary keys must be unique within the collection and this tool will
not work should primary keys be non-unique within the database query results.

Performance Testing
-------------------

I have not had the time to properly test this tool against a large dataset and
properly compile the data. This data should be coming soon...
