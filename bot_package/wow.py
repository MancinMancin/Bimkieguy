from discord.ext import commands

def setup(bot):
    bot.add_command(wa)
    bot.add_command(avd)

@commands.command()
async def wa(ctx):
    await ctx.send("**Dungeon Talent Reminder:**\n"
                   "<https://wago.io/Vt4e96WAA>\n\n"

                   "**Dungeon Teleports:**\n"
                   "<https://wago.io/aCa7oAT5y>")
    
@commands.command()
async def avd(ctx, *args):
    avoidable_damage = {
        1: {"Gnarlroot": {
            421898: True, # Flaming Pestilence
            422039: True, # Shadowflame Cleave
            421971: True, # Controlled Burn
            422023: True, # Shadow-Scorched Earth
            425648: True, # Doom Roots
            422373: True, # Toxic Loam
        }},
        2: {"Igira": {
            414770: True, # Blistering Torment
            416998: True, # Twisting Blade
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
            421020: False, # Agonizing Claws
        }},
        5: {"Larodar": {
            418535: True, # Explosive Bark
            426206: True, # Blazing Thorns 
            417610: True, # Burning Ground
            427434: True, # Fire Whirl
            421318: False, # Smoldering Backdraft
        }},
        6: {"Nymue": {
            429785: True, # Impending Loom
            430485: True, # Reclamation
            423369: True, # Barrier Blossom
            423993: True, # Dream Exhaust
            429108: True, # Lumbering Slam
            425370: True, # Radial Flourish
        }},
        7: {"Smolderon": {
            421961: True, # Flame Waves
            422691: True, # Lava Geysers
            421532: True, # Smoldering Ground
            422172: True, # World in Flames
            425574: True, # Lingering Burn
        }},
        8: {"Tindral": {
            422503: True, # Star Fragments
            424499: True, # Scorching Ground
            426687: False, # Poisonous Mushroom
            423264: False, # Blazing Mushroom
            427297: True, # Flame Surge
            420240: True, # Sunflame
            421398: True, # Fire Beam
            421939: True, # Scorching Plume
        }},
        9: {"Fyrakk": {
            419066: True, # Raging Flames
            428960: True, # Fyr'alath's Flame
            419506: True, # Firestorm
            425484: True, # Dark Embers
            425483: True, # Incinerated
            425345: True, # Fyr'alath's Flame
            410223: True, # Shadowflame Breath
            422518: True, # Greater Firestorm
            422524: True, # Shadowflame Devastation
            414186: True, # Blaze
            422935: True, # Eternal Firestorm
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