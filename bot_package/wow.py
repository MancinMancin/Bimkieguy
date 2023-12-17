from discord.ext import commands

def setup(bot):
    bot.add_command(wago)
    bot.add_command(avd)
    bot.add_command(defki)

@commands.command()
async def wago(ctx):
    await ctx.send("**Dungeon Talent Reminder:**\n"
                   "<https://wago.io/Vt4e96WAA>\n\n"

                   "**Dungeon Teleports:**\n"
                   "<https://wago.io/aCa7oAT5y>")
    
@commands.command()
async def avd(ctx, *args):
    avoidable_damage = {
        1: {"Gnarlroot": {
            421960: True, # Flaming Pestilence
            422039: True, # Shadowflame Cleave
            422023: True, # Shadow-Scorched Earth
            425648: True, # Doom Roots
            425659: True, # Doom Roots
            422373: True, # Toxic Loam
        }},
        2: {"Igira": {
            417003: True, # Twisting Blade
            424347: True, # Devastation
            426017: True, # Vital Rupture
        }},
        3: {"Volcoross": {
            421082: True, # Hellboil
            423494: True, # Tidal Blaze
            421616: True, # Volcanic Disgorge
        }},
        4: {"Council": {
            423551: True, # Whimsical Gust
            421032: True, # Captivating Finale
            421021: False, # Agonizing Claws
        }},
        5: {"Larodar": {
            418538: True, # Explosive Bark
            426209: True, # Blazing Thorns 
            429265: True, # Burning Ground
            427343: True, # Fire Whirl
            421591: False, # Smoldering Backdraft
        }},
        6: {"Nymue": {
            429785: True, # Impending Loom
            430485: True, # Reclamation
            423369: True, # Barrier Blossom
            423994: True, # Dream Exhaust
            428481: True, # Dream Exhaust v2
            429108: True, # Lumbering Slam
            425370: True, # Radial Flourish
        }},
        7: {"Smolderon": {
            421969: True, # Flame Waves
            422823: True, # Lava Geysers
            421532: True, # Smoldering Ground
            422243: True, # World in Flames
            425575: True, # Lingering Burn
        }},
        8: {"Tindral": {
            422503: True, # Star Fragments
            425451: True, # Scorching Ground
            426687: False, # Poisonous Mushroom
            424577: False, # Blazing Mushroom v1
            423264: False, # Blazing Mushroom v2
            427311: True, # Flame Surge
            423656: True, # Fire Beam v1
            423649: True, # Fire Beam v2
            421939: True, # Scorching Plume
        }},
        9: {"Fyrakk": {
            419504: True, # Raging Flames
            425345: True, # Fyr'alath's Flame
            420313: True, # Firestorm v1
            419061: True, # Firestorm v2
            425484: True, # Dark Embers
            425483: True, # Incinerated
            425345: False, # Fyr'alath's Flame
            410223: True, # Shadowflame Breath
            422522: True, # Greater Firestorm
            429956: True, # Shadowflame Devastation v1
            422526: True, # Shadowflame Devastation v2
            429782: True, # Eternal Firestorm
            425530: True, # Swirling Firestorm
        }}
    }
    message_to_send = []
    true_values = []
    false_values = []

    if not args:
        for _, inner_dict in avoidable_damage.items():
            for inner_key, inner_value in inner_dict.items():
                ability_ids = [key for key, value in inner_value.items() if value is True]
                false_ability_ids = [key for key, value in inner_value.items() if value is False]
                if false_ability_ids:
                    message_to_send.append(f"\n\n**{inner_key}:**\nability.id IN ({', '.join(map(str, ability_ids))}) OR target.role != \"tank\" AND ability.id IN ({', '.join(map(str, false_ability_ids))})")
                else:
                    message_to_send.append(f"\n\n**{inner_key}:**\nability.id IN ({', '.join(map(str, ability_ids))})")
                true_values.extend(ability_ids)
                false_values.extend(false_ability_ids)

        if false_values:
            false_values_line = " OR target.role != \"tank\" AND ability.id IN (" + ", ".join(map(str, false_values)) + ")"
            message_to_send.append(f"\n\n**All Bosses:**\nability.id IN ({', '.join(map(str, true_values))}){false_values_line}")
        else:
            message_to_send.append(f"\n\n**All Bosses:**\nability.id IN ({', '.join(map(str, true_values))})")

        await ctx.send("".join(message_to_send))
    else:
        selected_keys = []
        selected_true_values = []
        selected_false_values = []

        args = set(map(str, args))
        for outer_key, inner_dict in avoidable_damage.items():
            for inner_key, inner_value in inner_dict.items():
                if str(outer_key) in args:
                    ability_ids = [key for key, value in inner_value.items() if value is True]
                    if ability_ids:
                        selected_keys.append(inner_key)
                        selected_true_values.extend(ability_ids)
                    false_ability_ids = [key for key, value in inner_value.items() if value is False]
                    if false_ability_ids:
                        selected_false_values.extend(false_ability_ids)

        if selected_keys and selected_true_values:
            keys_line = ", ".join(map(str, selected_keys))
            true_values_line = "ability.id IN (" + ", ".join(map(str, selected_true_values)) + ")"
            if selected_false_values:
                false_values_line = " OR target.role != \"tank\" AND ability.id IN (" + ", ".join(map(str, selected_false_values)) + ")"
                message_to_send.append(f"\n\n**{keys_line}:**\n{true_values_line}{false_values_line}")
            else:
                message_to_send.append(f"\n\n**{keys_line}:**\n{true_values_line}")
            await ctx.send("".join(message_to_send))
        else:
            await ctx.send("Daj cyferki 1-9")

@commands.command()
async def defki(ctx):
    defensives = (

        # Death Knight
        48707, # Anti-Magic Shell
        48743, # Death Pact
        48792, # Icebound Fortitude
        327574, # Sacrificial Pact
        49998, # Death Strike

        # Demon Hunter
        198589, # Blur
        196555, # Netherwalk

        # Druid
        22812, # Barkskin
        108238, # Renewal
        61336, # Survival Instincts
        5487, # Bear Form

        # Evoker
        363916, # Obsidian Scales
        374348, # Renewing Blaze

        # Hunter
        186265, # Aspect of the Turtle
        109304, # Exhilaration
        264735, # Survival of the Fittest
        272679, # Fortitude of the Bear

        # Mage
        45438, # Ice Block
        414658, # Ice Cold
        342245, # Alter Time
        235313, # Blazing Barrier
        11426, # Ice Barrier
        235450, # Prismatic Barrier
        110959, # Greater Invisibility
        55342, # Mirror Image
    
        # Monk
        122470, # Touch of Karma
        122278, # Dampen Harm
        122783, # Diffuse Magic
        115203, # Fortifying Brew
        322101, # Expel Harm

        # Paladin
        642, # Divine Shield
        498, # Divine Protection (Holy)
        403876, # Divine Protection (Retribution)
        184662, # Shield of Vengeance

        # Priest
        19236, # Desperate Prayer
        47585, # Dispersion
        583, # Fade

        # Rogue
        31224, # Cloak of Shadows
        185311, # Crimson Vial
        5277, # Evasion
        1966, # Feint

        # Shaman
        108271, # Astral Shift
        198103, # Earth Elemental

        # Warlock
        108416, # Dark Pact
        104773, # Unending Resolve
        6789, # Mortal Coil

        # Warrior
        383762, # Bitter Immunity
        118038, # Die by the Sword
        184364, # Enraged Regeneration
        202168, # Impending Victory
        23920, # Spell Reflection
    )
    await ctx.send(f"ability.id IN {defensives}")