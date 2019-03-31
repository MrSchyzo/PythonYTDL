from optional import Optional


def assert_that(
        condition=True,
        assertion_title=""
):
    if not condition:
        raise RuntimeError(assertion_title + " did not happen")
    else:
        print(assertion_title + " happened!")


no_value = Optional.none()
some1 = Optional.of(1)
someObj = Optional.of({'a': 1, 'b': {'a': 1, 'b': None, 'c': {'a': 5}}})

assert_that(
    not no_value.map(lambda x: x + 1).has_value(),
    "None >>= (\\x -> x + 1) == None"
)
assert_that(
    no_value.or_else(2) == 2,
    "None orElse 2 == 2"
)
assert_that(
    some1.map(lambda x: -x).map(lambda x: x + 1).get_value() == 0,
    "Some(1) >>= (\\x -> -x) >>= (\\x -> x + 1) == Some(0)"
)
assert_that(
    some1.equals(Optional.of(1)),
    "Some(1) = Some(1)"
)
assert_that(
    not some1.map(lambda x: x * 5).filter(lambda x: x % 2 == 0).has_value(),
    "Some(1) >>= (\\x -> x * 5) filter (\\x -> x % 2 == 0) == None"
)
assert_that(
    some1.map(lambda _: None).equals(Optional.none()),
    "Some(1) >>= (\\x -> None) == None"
)
assert_that(
    someObj.map(lambda x: x['b']).map(lambda x: x['c']).map(lambda x: x['a']).equals(Optional.of(5)),
    "Optional map acting as null propagation"
)
assert_that(
    some1.map(Optional.of).equals(Optional.of(Optional.of(1))),
    "Optional map support for iterated \"functoriality\""
)
assert_that(
    some1.flat_map(Optional.of).equals(Optional.of(1)),
    "Optional flat_map's lifting property"
)