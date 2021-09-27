__all__ = ('extension',)

my_extension = tuple(
     f'{__name__}.{name}' for name in
         'cog_template',
)
addtional_extension = (
    'jishaku',
)
extension = my_extension + addtional_extension
