#python

import lx, lxu, modo, kelvin, traceback

NAME = kelvin.symbols.ARGS_NAME
MODE = kelvin.symbols.ARGS_MODE
OPERATION = kelvin.symbols.ARGS_OPERATION
CONNECTED = kelvin.symbols.ARGS_CONNECTED
PRESET = kelvin.symbols.ARGS_PRESET

AUTO_FILTER = kelvin.symbols.FILTER_TYPES_AUTO
MATERIAL = kelvin.symbols.FILTER_TYPES_MATERIAL
PART = kelvin.symbols.FILTER_TYPES_PART
PICK = kelvin.symbols.FILTER_TYPES_PICK

AUTO_OPERATION = kelvin.symbols.OPERATIONS_AUTO
ADD = kelvin.symbols.OPERATIONS_ADD
REMOVE = kelvin.symbols.OPERATIONS_REMOVE

NAME_CMD = kelvin.symbols.COMMAND_NAME_PTAG

class CMD_kelvin(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add(NAME, lx.symbol.sTYPE_STRING)
        self.dyna_Add(MODE, lx.symbol.sTYPE_STRING)
        self.dyna_Add(OPERATION, lx.symbol.sTYPE_STRING)
        self.dyna_Add(CONNECTED, lx.symbol.sTYPE_BOOLEAN)
        self.dyna_Add(PRESET, lx.symbol.sTYPE_STRING)

        for i in range(1,5):
            self.basic_SetFlags(i, lx.symbol.fCMDARG_OPTIONAL | lx.symbol.fCMDARG_HIDDEN)


    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO


    def basic_Execute(self, msg, flags):
        try:
            args = {}
            args[NAME] = self.dyna_String(0) if self.dyna_IsSet(0) else kelvin.defaults.get('ptag')
            args[MODE] = self.dyna_String(1) if self.dyna_IsSet(1) else AUTO_FILTER
            args[OPERATION] = self.dyna_String(2) if self.dyna_IsSet(2) else AUTO_OPERATION
            args[CONNECTED] = self.dyna_Bool(3) if self.dyna_IsSet(3) else False
            args[PRESET] = self.dyna_String(4) if self.dyna_IsSet(4) else None

            if args[NAME] == '':
                args[NAME] = kelvin.defaults.get('ptag')

            if args[MODE] == MATERIAL:
                LXi_POLYTAG = lx.symbol.i_POLYTAG_MATERIAL
            elif args[MODE] == PICK:
                LXi_POLYTAG = lx.symbol.i_POLYTAG_PICK
            else:
                LXi_POLYTAG = lx.symbol.i_POLYTAG_PART

            if args[OPERATION] == AUTO_OPERATION:
                if args[CONNECTED]:
                    kelvin.selection.tag_polys( args[NAME], True, LXi_POLYTAG )
                else:
                    kelvin.selection.tag_polys( args[NAME], False, LXi_POLYTAG )

                if (
                    not kelvin.shadertree.get_masks(pTags = {args[NAME]:LXi_POLYTAG})
                    and not args[NAME] == kelvin.defaults.get('ptag')
                    ):

                    mask = kelvin.shadertree.build_material(
                        i_POLYTAG = LXi_POLYTAG,
                        pTag = args[NAME],
                        preset = args[PRESET]
                    )

                    kelvin.shadertree.cleanup()
                    kelvin.shadertree.move_to_top(mask)

            if args[OPERATION] == ADD:
                if args[CONNECTED]:
                    kelvin.selection.tag_polys( args[NAME], True, LXi_POLYTAG )
                else:
                    kelvin.selection.tag_polys( args[NAME], False, LXi_POLYTAG )

                mask = kelvin.shadertree.build_material(
                    i_POLYTAG = LXi_POLYTAG,
                    pTag = args[NAME],
                    preset = args[PRESET]
                )

                kelvin.shadertree.cleanup()
                kelvin.shadertree.move_to_top(mask)

            if args[OPERATION] == REMOVE:
                if args[CONNECTED]:
                    kelvin.selection.tag_polys( kelvin.defaults.get('ptag'), True, LXi_POLYTAG )
                else:
                    kelvin.selection.tag_polys( kelvin.defaults.get('ptag'), False, LXi_POLYTAG )

                kelvin.shadertree.cleanup()

        except:
            traceback.print_exc()


lx.bless(CMD_kelvin, NAME_CMD)
