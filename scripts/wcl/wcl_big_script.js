
        var game_id = 0;
        var siteTitle = "Warcraft Logs";
        var currentLang = "en";
        var rankingsLabel = "Rankings";
        var report_id = 'R47AwfNhdXpgD38c';
        var zone_id = '47';
        var expired_state = 0;
        var subscribed = false;
        var report_name = "pavend - Personal Logs";
        var comparison_reports_string = '';
        var comparisonReports = []
        var comparisonCounts = []
        comparisonCounts[report_name] = 1
        var comparisonName
        
        var guildForReportFollowingDeletion = "/user/calendar/3083374";
        var start_time = 1780149401882;
        var end_time = 1780176422565;
        var graph_options = parseInt(33)
        var defaultFilterGraph = graph_options & 32
        var pin_options = parseInt(0)
        var wipe_options = parseInt(0)

        var usingMultiReportAnalysis = !!"";
        var mraFilters = ""

        var assetServer = "https://assets.rpglogs.com"

        var isReportAnonymous = false;

        const minimumUnmitigatedDamageLogVersion = 12;
        const minimumMitigationInHealingDoneLogVersion = 16;

        var icon_path = "https://assets.rpglogs.com/img/warcraft/";

        var abilityPath = 'https://www.wowhead.com/spell=';
        var buffPath = 'https://www.wowhead.com/spell=';
        var itemPath = 'https://www.wowhead.com/item=';
        var npcPath = 'https://www.wowhead.com/npc=';

        var abilityCutoff = 10;
        var buffCutoff = 0;

        
        function abilityExternalLink(id) {
            if (id < abilityCutoff)
                return '#';
            if (buffCutoff && id >= buffCutoff)
                return buffPath + (id - buffCutoff);
            return abilityPath + id;
        }

        function abilityExternalLinkForEntry(ability) {
            let linkID = ability.secondaryGameID ? ability.secondaryGameID : ability.guid
            return abilityExternalLink(linkID)
        }

        function buffExternalLink(id) {
            if (id < abilityCutoff)
                return '#';
            if (buffCutoff)
                return `${buffPath}${id - buffCutoff}`;
            return `${buffPath}${id}`; // id can be a string for some games with no buff cutoff.
        }

        function buffExternalLinkForEntry(ability) {
            let linkID = ability.secondaryGameID ? ability.secondaryGameID : ability.guid
            return buffExternalLink(linkID)
        }

        function itemExternalLink(id) {
            return itemPath + id;
        }

        function npcExternalLink(id) {
            return npcPath + id;
        }

        function computeDBSiteSlug(name) {
          return name
            .replace(/ \/ |\/| - |[:'(),?%]|\s+/g, (match) => {
              if (match === " / ") return " ";   // collapse " / " to space
              if (match === "/") return "-";     // convert lone slashes to dash
              if (match === " - ") return "-";   // space-dash-space to dash
              if (/\s+/.test(match)) return "-"; // spaces -> dash
              return "";                         // remove punctuation
            })
            .toLowerCase();
        }

        function npcExternalLinkForEntry(actor) {
            let linkID = actor.secondaryGameID ? actor.secondaryGameID : actor.guid
            return npcExternalLink(linkID) + (game_id === 7 ? '/' + computeDBSiteSlug(actor.name) : '');
        }

                    var localizedAffixes = { affix_1: { name: "Overflowing", "icon": "inv_misc_volatilewater.jpg" }, affix_2: { name: "Skittish", "icon": "spell_magic_lesserinvisibilty.jpg" }, affix_3: { name: "Volcanic", "icon": "spell_shaman_lavasurge.jpg" }, affix_4: { name: "Necrotic", "icon": "spell_deathknight_necroticplague.jpg" }, affix_5: { name: "Teeming", "icon": "spell_nature_massteleport.jpg" }, affix_6: { name: "Raging", "icon": "ability_warrior_focusedrage.jpg" }, affix_7: { name: "Bolstering", "icon": "ability_warrior_battleshout.jpg" }, affix_8: { name: "Sanguine", "icon": "spell_shadow_bloodboil.jpg" }, affix_9: { name: "Tyrannical", "icon": "achievement_boss_archaedas.jpg" }, affix_10: { name: "Fortified", "icon": "ability_toughness.jpg" }, affix_11: { name: "Bursting", "icon": "ability_ironmaidens_whirlofblood.jpg" }, affix_12: { name: "Grievous", "icon": "ability_backstab.jpg" }, affix_13: { name: "Explosive", "icon": "spell_fire_felflamering_red.jpg" }, affix_14: { name: "Quaking", "icon": "spell_nature_earthquake.jpg" }, affix_15: { name: "Relentless", "icon": "inv_chest_plate04.jpg" }, affix_16: { name: "Infested", "icon": "achievement_nazmir_boss_ghuun.jpg" }, affix_117: { name: "Reaping", "icon": "ability_racial_embraceoftheloa_bwonsomdi.jpg" }, affix_119: { name: "Beguiling", "icon": "spell_shadow_mindshear.jpg" }, affix_120: { name: "Awakened", "icon": "trade_archaeology_nerubian_obelisk.jpg" }, affix_121: { name: "Prideful", "icon": "spell_animarevendreth_buff.jpg" }, affix_122: { name: "Inspiring", "icon": "spell_holy_prayerofspirit.jpg" }, affix_123: { name: "Spiteful", "icon": "spell_holy_prayerofshadowprotection.jpg" }, affix_124: { name: "Storming", "icon": "spell_nature_cyclone.jpg" }, affix_128: { name: "Tormented", "icon": "spell_animamaw_orb.jpg" }, affix_129: { name: "Infernal", "icon": "inv_infernalbrimstone.jpg" }, affix_130: { name: "Encrypted", "icon": "spell_progenitor_orb.jpg" }, affix_131: { name: "Shrouded", "icon": "spell_shadow_nethercloak.jpg" }, affix_132: { name: "Thundering", "icon": "shaman_pvp_leaderclan.jpg" }, affix_133: { name: "Focused", "icon": "ability_mage_timewarp.jpg" }, affix_134: { name: "Entangling", "icon": "inv_misc_root_01.jpg" }, affix_135: { name: "Afflicted", "icon": "spell_misc_emotionsad.jpg" }, affix_136: { name: "Incorporeal", "icon": "achievement_boss_anomalus.jpg" }, affix_137: { name: "Shielding", "icon": "paladin_holy.jpg" }, affix_144: { name: "Thorned", "icon": "ability_demonhunter_demonspikes2.jpg" }, affix_145: { name: "Reckless", "icon": "ability_warrior_sunder.jpg" }, affix_146: { name: "Attuned", "icon": "spell_arcane_arcanepotency_nightborne.jpg" }, affix_147: { name: "Xal'atath's Guile", "icon": "ability_racial_chillofnight.jpg" }, affix_148: { name: "Xal'atath's Bargain: Ascendant", "icon": "inv_nullstone_cosmicvoid.jpg" }, affix_152: { name: "Challenger's Peril", "icon": "achievement_challengemode_everbloom_hourglass.jpg" }, affix_153: { name: "Xal'atath's Bargain: Frenzied", "icon": "spell_shadow_unholyfrenzy.jpg" }, affix_158: { name: "Xal'atath's Bargain: Voidbound", "icon": "inv_cosmicvoid_buff.jpg" }, affix_159: { name: "Xal'atath's Bargain: Oblivion", "icon": "spell_priest_void-blast.jpg" }, affix_160: { name: "Xal'atath's Bargain: Devour", "icon": "inv_ability_voidweaverpriest_entropicrift.jpg" }, affix_162: { name: "Xal'atath's Bargain: Pulsar", "icon": "inv_cosmicvoid_nova.jpg" }, affix_165: { name: "Lindormi's Guidance", "icon": "ability_evoker_bronze_01.jpg" }, affix_166: { name: "Eternus's Trial: Sands of Time", "icon": "item_enchantedpearl.jpg" }, affix_167: { name: "Eternus's Trial: Dusk of the Infinite", "icon": "achievement_boss_infinitecorruptor.jpg" }, affix_168: { name: "Eternus's Trial: Timeways Manifested", "icon": "spell_sandelemental.jpg" }, affix_169: { name: "Eternus's Trial: Twilight Reflections", "icon": "trade_archaeology_highbornesoulmirror.jpg" }, affix_170: { name: "Tyrannically Fortified", "icon": "inv_helm_laughingskull_01.jpg" }, affix_178: { name: "", "icon": "" }, }; function nameForAffix(affix) { return localizedAffixes["affix_" + affix] ? localizedAffixes["affix_" + affix].name : "Unknown"; }; function iconForAffix(affix) { return localizedAffixes["affix_" + affix] ? localizedAffixes["affix_" + affix].icon :  "inv_axe_02.jpg" }; 
        
        var extensionForActorIcons = ".jpg";
        const archived = false;
        var talentTreeBlueprintCache = {};
    