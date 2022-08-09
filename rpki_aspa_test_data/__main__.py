# Copyright (c) 2022 Ben Maddison. All rights reserved.
#
# The contents of this file are licensed under the MIT License
# (the "License"); you may not use this file except in compliance with the
# License.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""rpki_aspa_test_data cli interface."""

from __future__ import annotations

import logging
import sys
from typing import Optional

from rpkimancer.cert import CertificateAuthority, TACertificateAuthority

from rpkimancer_aspa.sigobj import Aspa

from .cli import parse_args
from .data import Cases

log = logging.getLogger(__name__)


def main() -> Optional[int]:
    """Generate a hierarchy of RPKI repos containing test ASPA objects."""
    try:
        args = parse_args()
        cases = Cases.load(args.test_cases, *args.extra_cases)
        log.info("creating TA")
        ta = TACertificateAuthority(as_resources=[(0, 4294967295)])
        for case in cases:
            log.info(f"creating CA '{case.ca_name}'")
            ca = CertificateAuthority(issuer=ta,
                                      common_name=case.ca_name,
                                      as_resources=[case.customer_asid])
            log.info(f"creating ASPA for case '{case}'")
            _ = Aspa(issuer=ca,
                     customer_as=case.customer_asid,
                     provider_as_set=case.providers)
        log.info("publishing objects")
        ta.publish(pub_path=args.output_path / "repo",
                   tal_path=args.output_path / "tals")
    except Exception as e:
        log.error(e)
        return 1
    return None


if __name__ == "__main__":
    sys.exit(main())
