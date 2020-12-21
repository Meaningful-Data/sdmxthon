from SDMXThon.model.structure import PrimaryMeasure


def get_series_groups(df, dsd):
    grouping_keys = dsd.dimensionCodes
    grouping_keys.remove('TIME_PERIOD')

    for e in dsd.attributeDescriptor.components.values():
        if e.id in df.keys() and e.relatedTo is not None and not isinstance(e.relatedTo, PrimaryMeasure):
            grouping_keys.append(e.id)
    count = 0
    for k, v in df.groupby(grouping_keys):
        count += 1
        if count < 10:
            print(f'[group {k}]')
            print(f'{v[["TIME_PERIOD", "OBS_STATUS", "OBS_CONF", "OBS_VALUE"]]}')
        else:
            break
