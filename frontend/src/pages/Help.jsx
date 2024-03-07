
function Help() {
  return (
    <div>
        <h1>How to connect your email to <span style={{fontWeight:'normal'}}>EmailTidy</span></h1>
        <p>In order to connect your email to EmailTidy using Yahoo or Google you'll need to create what's called a 3rd party app password. This password grants EmailTidy access to your inbox in order to scan for spam. Don't worry as this password is stored safely and is encrypted for your safety. EmailTidy will also NEVER store data collected from your inbox besides captured unsubscribe links found for the functionality of the app.</p>
        <br />
        <h2>Instructions</h2>
        <ul style={{listStyle:'disc'}}>
          <li>
            For instructions with Google visit <a style={{textDecoration:'underline'}} href='https://support.google.com/accounts/answer/185833?hl=en' target='_blank'>https://support.google.com/accounts/answer/185833?hl=en</a>
          </li>
          <li>
            For instructions with Yahoo visit <a href='https://help.yahoo.com/kb/SLN15241.html' target='_blank' style={{textDecoration:'underline'}}>https://help.yahoo.com/kb/SLN15241.html</a>
          </li>
          <li>
            If you aren't using Yahoo or Google you can also enter in the imap server URL to connect to manually. This will be located in your mail client's mail settings. If you don't know where that is try making a search on the internet <a href="https://search.brave.com/search?q=how+to+locate+imap+server+in+your+email+client&source=web" target="_blank" style={{textDecoration:'underline'}}>"how to locate imap server in my email client"</a>.
          </li>
        </ul>
    </div>
  )
}

export default Help