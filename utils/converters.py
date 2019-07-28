from discord.ext import commands


class Code(commands.Converter):
    async def convert(self, ctx, arg):
        return self.cleanup_code(arg)

    @staticmethod
    def cleanup_code(code):
        if code.startswith('```') and code.endswith('```'):
            return code.strip("```").strip("\n")
        return code.strip('\n')