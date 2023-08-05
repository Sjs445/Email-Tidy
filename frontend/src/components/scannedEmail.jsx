// TODO: If the user has unsubscribed already or attempted, do not show button

function ScannedEmail( {scanned_email} ) {
  return (
    <tbody>
        <tr>
            <td>{scanned_email.from}</td>
            <td>{scanned_email.subject}</td>
            <td>{scanned_email.link_count}</td>
            {scanned_email.link_count > 0 ? (
                <td><button className="btn">Unsubscribe</button></td>
            ) : <td><p>No unsubscribe link found</p></td>}
        </tr>
    </tbody>
  )
}

export default ScannedEmail