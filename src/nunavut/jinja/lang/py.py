#
# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# Copyright (C) 2018-2019  UAVCAN Development Team  <uavcan.org>
# This software is distributed under the terms of the MIT License.
#
"""
    jinja-based filters for generating python. All filters in this
    module will be available in the template's global namespace as ``py``.
"""
from nunavut.jinja.jinja2 import contextfilter
from nunavut.jinja.jinja2.runtime import Context


@contextfilter
def filter_to_template_unique_name(ctx: Context, base_token: str) -> str:
    """
    Jinja filter that takes a base token and forms a name that is very
    likely to be unique within the template the filter is invoked. This
    name is also very likely to be a valid Python identifier.

    .. IMPORTANT::

        The exact tokens generated may change between major or minor versions
        of this library. The only guarantee provided is that the tokens
        will be stable for the same version of this library given the same
        input.

        Also note that name uniqueness is only likely within a given template.
        Between templates there is no guarantee of uniqueness and,
        since this library does not lex generated source, there is no guarantee
        that the generated name does not conflict with a name generated by
        another means.

    Example::

        {{ "foo" | py.to_template_unique_name }}
        {{ "foo" | py.to_template_unique_name }}
        {{ "bar" | py.to_template_unique_name }}
        {{ "i like coffee" | py.to_template_unique_name }}

    Results Example::

        # These are the likely results but the specific token
        # generatted is not strongly specified.
        _foo0_
        _foo1_
        _bar0_
        _i like coffee0_ # Note that this is not a valid python identifier.
                         # This filter does _not_ lex the base_token argument.


    :param str base_token: A token to include in the base name.
    :returns: A name that is likely to be valid python identifier and is likely to
        be unique within the file generated by the current template.
    """
    return ctx.environment.globals['_unique_name_generator']('py', ctx.name, base_token, '_', '_')  # type: ignore