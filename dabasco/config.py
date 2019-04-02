from string import Template

#####################################
# DABASCO API: input keywords
DABASCO_INPUT_KEYWORD_OPINION_NONE = 'none'
DABASCO_INPUT_KEYWORD_OPINION_WEAK = 'weak'
DABASCO_INPUT_KEYWORD_OPINION_STRONG = 'strong'
DABASCO_INPUT_KEYWORD_OPINION_STRICT = 'strict'
DABASCO_INPUT_KEYWORD_DISCUSSION_ID = 'discussion'
DABASCO_INPUT_KEYWORD_TYPE = 'type'
DABASCO_INPUT_KEYWORD_ASSUMPTIONS = 'assumptions'
DABASCO_INPUT_KEYWORD_BIAS = 'bias'
DABASCO_INPUT_KEYWORD_POSITIVE_BIAS = 'positive'
DABASCO_INPUT_KEYWORD_NEGATIVE_BIAS = 'negative'
DABASCO_INPUT_KEYWORD_OPINION = 'opinion'
DABASCO_INPUT_KEYWORD_USER = 'user'
DABASCO_INPUT_KEYWORD_SEMANTICS = 'semantics'

# DABASCO API: output keywords
DABASCO_OUTPUT_KEYWORD_DISCUSSION_ID = 'dbas_discussion_id'
DABASCO_OUTPUT_KEYWORD_USER_ID = 'dbas_user_id'
DABASCO_OUTPUT_KEYWORD_ADF = 'adf'
DABASCO_OUTPUT_KEYWORD_AF = 'af'

DUMMY_LITERAL_NAME_OPINION = 'opinion_dummy'
DUMMY_LITERAL_NAME_ASSUMPTIONS = 'assumptions_dummy'

LITERAL_PREFIX_OPINION_ASSUME = 'ua'             # read "user accepts"
LITERAL_PREFIX_OPINION_REJECT = 'ur'             # read "user rejects"
LITERAL_PREFIX_ASSUMPTION_ASSUME = 'a'           # read "accept"
LITERAL_PREFIX_ASSUMPTION_REJECT = 'r'           # read "reject"
LITERAL_PREFIX_STATEMENT = 's'                   # read "statement"
LITERAL_PREFIX_INFERENCE_RULE = 'i'              # read "inference"
LITERAL_PREFIX_NOT = 'n'                         # read "not"


#####################################
# DBAS API: version (1 or 2)
DBAS_API_VERSION = 1

# DBAS API: URL schema
DBAS_BASE_URL = 'http://localhost:4284'
DBAS_API1_BASE_PATH = '/export'
DBAS_API1_PATH_GRAPH_DATA = 'doj'
DBAS_API1_PATH_USER_DATA = 'doj_user'
DBAS_API2_BASE_PATH = '/api/v2/query'

# DBAS API v2: interface keywords
DBAS_API2_QUERY_KEY = 'q'
DBAS_API2_QUERY_STATEMENTS = Template('''
{
  issue(uid: $discussion_id) {
    statements {
      uid
    }
  }
}
''')
DBAS_API2_QUERY_ARGUMENTS = Template('''
{
  issue(uid: $discussion_id) {
    arguments {
      uid
      isSupportive
      premisegroup {
        premises {
          statementUid
        }
      }
      conclusionUid
      argumentUid
    }
  }
}
''')
DBAS_API2_QUERY_OPINION = Template('''
{
  user(uid: $user_id) {
    clickedStatements(isValid: true) {
      statement {
        uid
        isUpvote
      }
    }
  }
}
''')

# DBAS API v1: interface keywords
DBAS_KEYWORD_ACCEPTED_STATEMENTS_EXPLICIT = 'marked_statements'
DBAS_KEYWORD_ACCEPTED_STATEMENTS_IMPLICIT = 'accepted_statements_via_click'
DBAS_KEYWORD_REJECTED_STATEMENTS_IMPLICIT = 'rejected_statements_via_click'
DBAS_KEYWORD_ACCEPTED_ARGUMENTS_EXPLICIT = 'marked_arguments'
DBAS_KEYWORD_REJECTED_ARGUMENTS_EXPLICIT = 'rejected_arguments'

DBAS_KEYWORD_STATEMENTS = 'nodes'
DBAS_KEYWORD_INFERENCE_RULES = 'inferences'
DBAS_KEYWORD_INFERENCE_RULE_ID = 'id'
DBAS_KEYWORD_INFERENCE_RULE_PREMISES = 'premises'
DBAS_KEYWORD_INFERENCE_RULE_CONCLUSION = 'conclusion'
DBAS_KEYWORD_INFERENCE_RULE_SUPPORTIVE = 'is_supportive'
DBAS_KEYWORD_UNDERCUTS = 'undercuts'
DBAS_KEYWORD_UNDERCUT_ID = 'id'
DBAS_KEYWORD_UNDERCUT_PREMISES = 'premises'
DBAS_KEYWORD_UNDERCUT_CONCLUSION = 'conclusion'


#####################################
# TOAST API: interface keywords
TOAST_SYMBOL_RULE_DEFEASIBLE = '=>'
TOAST_SYMBOL_RULE_STRICT = '->'
TOAST_SYMBOL_NEGATION = '~'
TOAST_SYMBOL_PREFERENCE = '<'
TOAST_SYMBOL_RULE_NAME_PREFIX = '['
TOAST_SYMBOL_RULE_NAME_SUFFIX = ']'

TOAST_KEYWORD_ASSUMPTIONS = 'assumptions'
TOAST_KEYWORD_AXIOMS = 'axioms'
TOAST_KEYWORD_RULES = 'rules'
TOAST_KEYWORD_RULEPREFS = 'rulePrefs'
TOAST_KEYWORD_LITERALPREFS = 'kbPrefs'
TOAST_KEYWORD_LINK_PRINCIPLE = 'link'
TOAST_KEYWORD_CONTRARINESS = 'contrariness'
TOAST_KEYWORD_SEMANTICS = 'semantics'

TOAST_KEYWORD_LAST_LINK_PRINCIPLE = 'last'
TOAST_KEYWORD_WEAKEST_LINK_PRINCIPLE = 'weakest'

TOAST_KEYWORD_SEMANTICS_PREFERRED = 'preferred'
TOAST_KEYWORD_SEMANTICS_STABLE = 'stable'
TOAST_KEYWORD_SEMANTICS_GROUNDED = 'grounded'
