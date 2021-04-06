# what is this

The methods translating dBase-to-DataFrame, DataFrame-to-dBase.

## how to use

```python
# read dBase file as DataFrame
dbf_df = dbf2df('./sample.dbf')
```

```python
# write DataFrame as dBase file
dbf2df(dbf_df, './output.dbf')
```

## dependencies

-   libpysal
-   pandas

## license

-   MIT
