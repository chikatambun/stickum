# New Features #
List of features that are being evaluated and implemented for future stickum releases.

## Port to Genshi ##
Genshi is quicker and has some nice features that kid lacks.  Fedora has a genshi port already but it contains Fedora specific elements.  Need to merge those changes back to mainline.

## Make it easier to retheme ##
  * There are currently a few hardcoded paths in stickum.  Need to make those settable via config variables.  Use tg.url() in places so that we can operate under a subdirectory (useful when proxying to stickum).
  * Fedora has a stickum instance that uses CSS to retheme the visual style.  Need to merge any changes to the html templates to make this possible.  Maybe release a default css theme as well so people know what's available to change.

## Bugzilla/trac Integration ##
Have a simple interface for adding a paste to an existing bugzilla or trac bug.

### Initial Implementation ###
  * Site administrator can configure a list of bugzilla/trac instances with their name, base url, and "plugin" for accessing them.
  * User is shown a dropdown to select a bugzilla/trac instance, an entry to type in bug#, and a checkbox to add as attachment or inline.
  * The list of bugzillas/trac should specify whether the bugzilla needs to have an account.  If so, user must be logged into stickum to send a paste to a bug report.

### Possible Directions ###
**Note**: Reevaluate these after seeing how the initial implementation works.
  * Plugin architecture.  We'll want things like add\_as\_comment(), add\_as\_attachment(), authenticated(), register\_user()
  * Keep the list of bugzilla/trac instances in the db.  Allow changing the list via a web interface.  Possibly expose this to the user.
  * Have a way to store ids for bugzilla/trac in identity.  This will be the hardest one as there's no guarantee that information used to register with stickum is the same as used for these bugzilla/trac instances.